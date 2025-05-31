# Aegis Nexus Next.js

A modern AI-powered dashboard built with Next.js, TypeScript, and NLUX integration featuring a dark theme and responsive design.

## Features

- 🎨 Dark theme with customizable UI components
- 🤖 AI chat interface powered by NLUX
- 📱 Responsive sidebar navigation
- ⚡ Streaming and single response modes
- 🔧 Configurable settings panel
- 👥 AI agents management dashboard

## Tech Stack

- **Framework**: Next.js 15.3.3
- **Runtime**: React 18.3.1
- **Language**: TypeScript
- **AI Integration**: NLUX React Components
- **Icons**: React Icons
- **HTTP Client**: Axios

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository and navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
Create a `.env.local` file in the root directory:
```env
NEXT_PUBLIC_NLUX_API_KEY=<YOUR_KEY>
NEXT_PUBLIC_NLUX_API_URL=https://api.nlux.com/v1/chat
NEXT_PUBLIC_NLUX_MODE=stream
```

4. Start the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── components/
│   ├── ChatBox.tsx          # AI chat interface component
│   ├── Layout.tsx           # Main layout wrapper
│   └── Sidebar.tsx          # Collapsible navigation sidebar
├── pages/
│   ├── api/
│   │   └── chat.ts          # Chat API endpoint
│   ├── _app.tsx             # App wrapper with Layout
│   ├── index.tsx            # Dashboard homepage
│   ├── agents.tsx           # AI agents management
│   ├── chat.tsx             # Chat interface page
│   └── settings.tsx         # Application settings
├── styles/
│   └── globals.css          # Global dark theme styles
├── .env.local               # Environment configuration
└── package.json
```

## Configuration

### Environment Variables

- `NEXT_PUBLIC_NLUX_API_KEY`: Your NLUX API authentication key
- `NEXT_PUBLIC_NLUX_API_URL`: NLUX API endpoint URL
- `NEXT_PUBLIC_NLUX_MODE`: Response mode (`stream` or `single`)

### Theme Customization

The dark theme uses CSS custom properties defined in `styles/globals.css`:

```css
:root {
  --bg: #111;        /* Primary background */
  --panel: #222;     /* Panel/card background */
  --hover: #333;     /* Hover states */
  --text: #eee;      /* Primary text */
  --border: #444;    /* Border color */
  --accent: #555;    /* Accent color */
}
```

## API Integration

The chat functionality integrates with NLUX API through `/api/chat` endpoint which supports:

- **Streaming Mode**: Real-time response streaming
- **Single Mode**: Complete response delivery
- **Error Handling**: Graceful error management
- **Mock Responses**: Development-friendly fallbacks

## Navigation

The collapsible sidebar provides navigation to:

- **Dashboard**: System overview and status cards
- **Agents**: AI agent management interface  
- **Chat**: Interactive AI conversation interface
- **Settings**: Application configuration panel

## Development

### Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

### Code Style

- TypeScript for type safety
- React functional components with hooks
- CSS-in-JS for component styling
- Consistent naming conventions

## Production Deployment

1. Build the application:
```bash
npm run build
```

2. Start the production server:
```bash
npm start
```

3. Configure your NLUX API credentials in production environment.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.