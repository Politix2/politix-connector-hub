# Welcome to your Lovable project

## Project info

**URL**: https://lovable.dev/projects/240a43d8-eec0-45ca-8af9-10febf310c6c

## How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

Simply visit the [Lovable Project](https://lovable.dev/projects/240a43d8-eec0-45ca-8af9-10febf310c6c) and start prompting.

Changes made via Lovable will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with .

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/240a43d8-eec0-45ca-8af9-10febf310c6c) and click on Share -> Publish.

## I want to use a custom domain - is that possible?

We don't support custom domains (yet). If you want to deploy your project under your own domain then we recommend using Netlify. Visit our docs for more details: [Custom domains](https://docs.lovable.dev/tips-tricks/custom-domain/)

## Docker Deployment

### Building the Docker Image

1. Build the image from the project root directory:
   ```bash
   docker build -t politix-backend:latest .
   ```

2. Run locally with environment variables:
   ```bash
   docker run -p 8000:8000 \
     -e MISTRAL_API_KEY=your_mistral_api_key \
     -e SUPABASE_URL=your_supabase_url \
     -e SUPABASE_KEY=your_supabase_key \
     politix-backend:latest
   ```

## Deploying to RunPod

1. Push your Docker image to a registry (Docker Hub, GitHub Container Registry, etc.):
   ```bash
   # Tag your image
   docker tag politix-backend:latest your-registry/politix-backend:latest
   
   # Push to registry
   docker push your-registry/politix-backend:latest
   ```

2. Create a new pod on RunPod:
   - Select a template that includes GPU if needed
   - Set container image to your registry path
   - Add required environment variables:
     - `MISTRAL_API_KEY`
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
   - Expose port 8000

3. Start the pod and access your API at the provided URL.
