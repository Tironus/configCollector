from deviceCommander import DeviceConfig
import collectorGenerator
import models
import ipaddress
import os
import requests
import json


class configCollector():
	def __init__(self, device_data):
		os.environ["CONFIG_COMMANDER"] = "192.168.20.240"
		os.environ["CONFIG_COMMANDER_PORT"] = "8000"

		if isinstance(device_data, dict):
			self.device_data = device_data
		else:
			self.device_data = device_data.dict()
		cwdir = os.getcwd()
		if "tests" in os.getcwd() or "api" in os.getcwd():
			split_dir = cwdir.split('/')
			split_dir.pop(-1)
			cwdir = ('/').join(split_dir)

		os.environ['APP_DIR'] = cwdir

	def getConfig(self):
		d = DeviceConfig(
			self.device_data['device']['hostname'],
			self.device_data['device']['username'],
			self.device_data['device']['password'],
		)

		cg_data = collectorGenerator.collectorGenerator(self.device_data)
		cmds = cg_data.generateCommands()
		try:
			d.runCommands(cmds)
		except Exception:  # pylint: disable=broad-except
			return "device error", "failed", "failed to connect to device."

		for result in d.cmd_results:
			if d.cmd_results[result]['submit_config_result'] != 'success':

				_err_msg = "new configuration transaction failed, config backed out"
				return d.cmd_results, "failed", _err_msg
			output = d.cmd_results[result]['device_output'].splitlines()

		# build entities
		intf_entities = []
		interfaces_to_update = []
		for idx, cmd in enumerate(output):
			interface_output_start = 0
			if 'config system interface' in cmd:
				interface_output_start = idx
				for i, intf in enumerate(output[interface_output_start:]):
					if 'edit' in intf:
						list_ref = output[interface_output_start:]
						port_id = intf.split('"')[1]
						for id in range(i, i + 75):
							if 'set ip ' in list_ref[id]:
								ip = list_ref[id].split(' ')[2]
								netmask = list_ref[id].split(' ')[3]
								pfx_len = ipaddress.IPv4Network(f'0.0.0.0/{netmask}').prefixlen
								interface_entity = models.InterfaceParams(id=port_id, ipv4_address=ip, ipv4_prefix_len=pfx_len)
								intf_entities.append(interface_entity)
								continue
					if 'next' in intf:
						list_ref = output[interface_output_start:]
						if 'end' in list_ref[i+1]:
							break

		for entity in intf_entities:
			entity_dict = entity.dict()
			for intf in self.device_data["device"]["configuration"]["interfaces"]:
				if entity_dict["id"] == intf["id"]:
					if entity_dict["ipv4_address"] != intf["ipv4_address"] or \
							entity_dict["ipv4_prefix_len"] != intf["ipv4_prefix_len"]:

						entity.ipv4_address = intf["ipv4_address"]
						entity.ipv4_prefix_len = intf["ipv4_prefix_len"]
						interfaces_to_update.append(entity)
						continue


		if len(interfaces_to_update) > 0:
			intf_values = models.InterfaceValues(interfaces=interfaces_to_update)
			device_auth = models.DeviceAuth(
				hostname=self.device_data["device"]["hostname"],
				username=self.device_data["device"]["username"],
				password=self.device_data["device"]["password"],
				device_type=self.device_data["device"]["device_type"],
				firmware_version=self.device_data["device"]["firmware_version"],
				configuration=intf_values
			)
			device = models.Device(device=device_auth)
			return device.dict(), "success", "updates found"
		else:
			return {}, "noop", "no updates found"

	def process_config_diff(self):
		device_diff, status, msg = self.getConfig()
		headers = {"Content-Type": "application/json"}

		if status == "success":
			r = requests.post(
				f"http://{os.environ['CONFIG_COMMANDER']}:{os.environ['CONFIG_COMMANDER_PORT']}/config_device",
				headers=headers,
				data=json.dumps(device_diff)
			)
			return r.status_code, "success", r.text
		elif status == "noop":
			return "noop", "success", "no updates required"
		else:
			return "fail", "failed", "process_config_diff failed"