import os
from jinja2 import Environment, FileSystemLoader

class collectorGenerator():
	def __init__(self, device_data):
		if isinstance(device_data, dict):
			self.device_data = device_data
		else:
			self.device_data = device_data.dict()
		self.commands = []
		cwdir = os.getcwd()
		if "tests" in os.getcwd() or "api" in os.getcwd():
			split_dir = cwdir.split('/')
			split_dir.pop(-1)
			cwdir = ('/').join(split_dir)

		os.environ['APP_DIR'] = cwdir

	def get_config(self, template_path):
		params = {}
		params["interface"] = False

		command_list = []
		template_name = None

		file_loader = FileSystemLoader(template_path)
		env = Environment(loader=file_loader, keep_trailing_newline=True, trim_blocks=True)


		if self.device_data["device"]["device_type"] == "fortigate":
			template = env.get_template("fortigate_base")

			if "interfaces" in self.device_data["device"]["configuration"].keys():
				params["interface"] = True

			if "static_routes" in self.device_data["device"]["configuration"].keys():
				params["static_routes"] = True

			command_list.append(template.render(params=params))

		self.commands = command_list


	def generateCommands(self):
		app_dir = os.getenv("APP_DIR")

		if self.device_data['device']['device_type'] == 'fortigate':
			template_path = f"{app_dir}/command_templates/fortigate"
			self.get_config(template_path)

		return self.commands
