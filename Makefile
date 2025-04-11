.PHONY: create-vevn
create-vevn:
	@echo "Creating virtual environment"
	@python3 -m venv venv

.PHONY: activate-venv
activate-venv:
	@echo "Activating virtual environment"
	@source venv/bin/activate

.PHONY: install
install:
	@echo "Installing requirements"
	@pip install -r requirements.txt
	@echo "Virtual environment created and activated"

.PHONY: run
run:
	@echo "Running the application"
	@PYTHONPATH=. streamlit run app/ui/dashboard.py

.PHONY: docker-build
docker-build:
	@echo "🚧 Building Docker image for linux/amd64"
	@docker build --platform=linux/amd64 -t query-optimizer .

.PHONY: docker-run
docker-run:
	@echo "🐳 Running Docker container on http://localhost:8080"
	@docker run --rm \
		--env GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json \
		-v $(PWD)/credential/service-account.json:/app/service-account.json \
		-p 8080:8080 \
		query-optimizer

.PHONY: docker-run-cloud-run
docker-run-cloud-run:
	@echo "🐳 Running Docker container on http://localhost:8080"
	@docker run --rm \
		--env GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json \
		-v $(PWD)/credential/service-account.json:/app/service-account.json \
		-p 8080:8080 \
		us-central1-docker.pkg.dev/yams-lab-nonprod/query-optimizer/query-optimizer-ai

.PHONY: create-artifact-repo
create-artifact-repo:
	@echo "🗂️ Creating Artifact Registry repository..."
	@gcloud artifacts repositories create query-optimizer \
		--repository-format=docker \
		--location=us-central1 \
		--project=yams-lab-nonprod \
		--description="Query Optimizer AI container repository"

.PHONY: docker-tag-push
docker-tag-push:
	@echo "🐳 Tagging and pushing Docker image..."
	@IMAGE_URL=us-central1-docker.pkg.dev/yams-lab-nonprod/query-optimizer/query-optimizer-ai; \
	docker build --platform=linux/amd64 -t $$IMAGE_URL .; \
	docker push $$IMAGE_URL

.PHONY: check-env
check-env:
	@if [ -z "$(DD_API_KEY)" ]; then \
		echo "❌ DD_API_KEY is not set. Please define it in your .env file."; \
		exit 1; \
	fi; \
	if [ -z "$(DD_APP_KEY)" ]; then \
		echo "❌ DD_APP_KEY is not set. Please define it in your .env file."; \
		exit 1; \
	fi

.PHONY: deploy-cloud-run
deploy-cloud-run: check-env
	@echo "🚀 Deploying to Cloud Run in yams-lab-nonprod"
	@IMAGE_URL=us-central1-docker.pkg.dev/yams-lab-nonprod/query-optimizer/query-optimizer-ai; \
	gcloud run deploy query-optimizer-ai \
		--image=$$IMAGE_URL \
		--region=us-central1 \
		--platform=managed \
		--allow-unauthenticated \
		--set-env-vars="DD_API_KEY=$(DD_API_KEY),DD_APP_KEY=$(DD_APP_KEY)"

.PHONY: deploy
deploy: docker-tag-push deploy-cloud-run
	@echo "✅ Full deploy completed!"

.PHONY: docker-rmi
docker-rmi:
	@echo "🧹 Removing local Docker image from Artifact Registry"
	@docker rmi us-central1-docker.pkg.dev/yams-lab-nonprod/query-optimizer/query-optimizer-ai || true

.PHONY: clean
clean:
	@echo "🧽 Cleaning up..."
	@echo "→ Removing virtual environment..."
	@rm -rf venv
	@echo "→ Removing local Docker image..."
	@docker rmi query-optimizer || true
	@docker rmi us-central1-docker.pkg.dev/yams-lab-nonprod/query-optimizer/query-optimizer-ai || true
	@echo "→ Removing dangling Docker images and stopped containers..."
	@docker system prune -f

.PHONY: help
help:
	@echo "📘 Makefile commands:"
	@echo "  create-vevn:          --> Create a virtual environment"
	@echo "  activate-venv:        --> Activate the virtual environment"
	@echo "  install:              --> Install required packages"
	@echo "  run:                  --> Run the Streamlit application"
	@echo "  docker-build:         --> Build Docker image"
	@echo "  docker-run:           --> Run Docker container locally on :8080"
	@echo "  docker-run-cloud-run: --> Run pushed Cloud Run image locally"
	@echo "  docker-rmi:           --> Remove local Docker image"
	@echo "  create-artifact-repo: --> Create Artifact Registry repository"
	@echo "  docker-tag-push:      --> Tag and push Docker image to Artifact Registry"
	@echo "  deploy-cloud-run:     --> Deploy image to Cloud Run"
	@echo "  deploy:               --> Tag, push and deploy to Cloud Run"
	@echo "  clean:                --> Remove venv, local images and prune Docker system"
