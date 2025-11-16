# Environment Setup for Client

## API Configuration

To connect the frontend to the backend API, create a `.env.local` file in the `/client` directory:

```bash
cd client
touch .env.local
```

Add the following content to `.env.local`:

```env
# API Configuration
# URL of the LangGraph Testing Platform API
# Use port 8001 if port 8000 is already in use
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## Default Behavior

If `.env.local` is not created, the app will default to:

- API URL: `http://localhost:8000`

The app will automatically fall back to mock data if the API is not available.

## Custom API URL

If your API is running on a different host or port, update the `NEXT_PUBLIC_API_URL` value:

```env
NEXT_PUBLIC_API_URL=http://your-api-host:port
```

## Note

The `.env.local` file is gitignored and should not be committed to version control.
