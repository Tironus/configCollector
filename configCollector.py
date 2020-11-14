from deviceCommander import DeviceConfig
import collectorGenerator
import os

class configCollector():
	def __init__(self, device_data):
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

	def runConfig(self):
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
			output = d.cmd_results[result]['device_output']
		return d.cmd_results, "success", output
