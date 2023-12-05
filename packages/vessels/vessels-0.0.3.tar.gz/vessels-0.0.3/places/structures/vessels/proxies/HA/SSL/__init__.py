

'''
import vessels.proxies.HA.SSL as HA_SSL
HA_SSL.build_papers (
	certificate_path = "/etc/haproxy/SSL/certificate.pem",
	key_path = "certificate.pem.key"
)
'''

import os

def build_papers (
	certificate_path = "",
	key_path = "",
	
	days = "20000"
):

	assert (len (certificate_path) >= 1);
	assert (len (key_path) >= 1);
	
	script = " ".join ([
		"openssl req -x509 -newkey rsa:4096",
		f"-keyout '{ key_path }'",
		f"-out '{ certificate_path }'",
		f'-sha256 -days { days } -nodes -subj "/C=/ST=/L=/O=/OU=/CN="'
	])

	os.system (script)
	
	return;