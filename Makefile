.PHONY create-vevn:
create-vevn:
	@echo "Creating virtual environment"
	@python3 -m venv venv

.PHONY activate-venv:
activate-venv:
	@echo "Activating virtual environment"
	@source venv/bin/activate

.PHONY install:
install:
	@echo "Installing requirements"
	@pip install -r requirements.txt
	@echo "Virtual environment created and activated"

.PHONY run:
run:
	@echo "Running the application"
	@streamlit run app/ui/dashboard.py

.PHONY help:
help:
	@echo "Makefile commands:"
	@echo "  create-vevn: 		-->	Create a virtual environment"
	@echo "  activate-venv: 	-->	Activate the virtual environment"
	@echo "  install: 		-->	Install required packages"
	@echo "  run: 			-->	Run the Streamlit application"
	@echo "  help:			-->	Show this help message"