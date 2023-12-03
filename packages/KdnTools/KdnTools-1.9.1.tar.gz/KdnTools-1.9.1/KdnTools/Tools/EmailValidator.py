import logging
import re
import smtplib
import asyncio
import aiodns
import selectors


class EmailValidator:
    def __init__(self, concurrency_limit=100):
        self.EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        self.MX_DNS_CACHE = {}
        self.VALIDATION_CACHE = {}
        self.logger = logging.getLogger(__name__)
        self.setup_logger()
        self.selector = selectors.SelectSelector()
        self.loop = asyncio.SelectorEventLoop(self.selector)
        asyncio.set_event_loop(self.loop)
        self.semaphore = asyncio.Semaphore(concurrency_limit)

    def validate(self, emails, timeout=None, verify=True, debug=False):
        if debug:
            self.logger.setLevel(logging.DEBUG)

        if isinstance(emails, str):
            emails = [emails]

        results = []
        for email in emails:
            if not re.match(self.EMAIL_REGEX, email):
                results.append(False)
            else:
                result = self.loop.run_until_complete(self._verify_email(email, timeout, verify))
                results.append(result)

        return results

    def setup_logger(self):
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    async def get_mx_ip(self, hostname):
        if hostname not in self.MX_DNS_CACHE:
            try:
                resolver = aiodns.DNSResolver()
                self.MX_DNS_CACHE[hostname] = await resolver.query(hostname, "MX")
            except aiodns.error.DNSError:
                self.MX_DNS_CACHE[hostname] = None
        return self.MX_DNS_CACHE[hostname]

    async def get_mx_hosts(self, email):
        hostname = email[email.find("@") + 1:]
        if hostname in self.MX_DNS_CACHE:
            mx_hosts = self.MX_DNS_CACHE[hostname]
        else:
            mx_hosts = await self.get_mx_ip(hostname)
        return mx_hosts

    async def handler_verify(self, mx_hosts, email, timeout=None):
        for mx in mx_hosts:
            res = await self.network_calls(mx, email, timeout)
            if res:
                return res
        return False

    async def syntax_check(self, email):
        if re.match(self.EMAIL_REGEX, email):
            return True
        return False

    async def _verify_email(self, email, timeout=None, verify=True):
        if email in self.VALIDATION_CACHE:
            return self.VALIDATION_CACHE[email]

        is_valid_syntax = await self.syntax_check(email)
        if is_valid_syntax:
            if verify:
                mx_hosts = await self.get_mx_hosts(email)
                if mx_hosts is None:
                    self.VALIDATION_CACHE[email] = False
                    return False
                else:
                    result = await self.handler_verify(mx_hosts, email, timeout)
                    self.VALIDATION_CACHE[email] = result
                    return result
        else:
            self.VALIDATION_CACHE[email] = False
            return False

    def validate(self, emails, timeout=None, verify=True, debug=False):
        if debug:
            self.logger.setLevel(logging.DEBUG)

        if isinstance(emails, str):
            emails = [emails]

        tasks = [self._verify_email(email, timeout, verify) for email in emails]
        return self.loop.run_until_complete(asyncio.gather(*tasks))

    async def network_calls(self, mx, email, timeout=None):
        async with self.semaphore:
            try:
                smtp = smtplib.SMTP(timeout=timeout)
                smtp.set_debuglevel(False)
                smtp.connect(mx.host, 25)  # Use default SMTP port 25
                smtp.helo()
                smtp.mail("")
                code, message = smtp.rcpt(email)
                smtp.quit()
                if code == 250:
                    return True
                else:
                    return False
            except smtplib.SMTPConnectError:
                self.logger.error(f"Failed to connect to the server: {mx.host}")
            except smtplib.SMTPServerDisconnected:
                self.logger.error(f"Server disconnected: {mx.host}")
            except smtplib.SMTPResponseException as e:
                self.logger.error(f"SMTP error code: {e.smtp_code}, message: {e.smtp_error}")
            except smtplib.SMTPException:
                self.logger.error("SMTP error occurred.")
            except Exception as e:
                self.logger.error(f"An unexpected error occurred: {str(e)}")
            return False
