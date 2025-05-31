import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { message } = req.body;

  if (!message) {
    return res.status(400).json({ error: 'Message is required' });
  }

  const mode = process.env.NEXT_PUBLIC_NLUX_MODE || 'single';
  // const apiUrl = process.env.NEXT_PUBLIC_NLUX_API_URL;
  // const apiKey = process.env.NEXT_PUBLIC_NLUX_API_KEY;

  try {
    if (mode === 'stream') {
      // Set headers for streaming
      res.setHeader('Content-Type', 'text/plain');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');

      // Mock streaming response for demo purposes
      // In production, you would make an actual API call to NLUX
      const words = `I understand you want to chat. This is a mock response that demonstrates streaming. Each word appears gradually to simulate real-time AI responses from the NLUX API.`.split(' ');
      
      for (let i = 0; i < words.length; i++) {
        const chunk = i === 0 ? words[i] : ` ${words[i]}`;
        res.write(chunk);
        
        // Simulate streaming delay
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      
      res.end();
    } else {
      // Single response mode
      // Mock single response for demo purposes
      // In production, you would make an actual API call to NLUX
      const mockResponse = {
        message: `I received your message: "${message}". This is a mock response. To use real NLUX API, please configure your API key and endpoint in the .env.local file.`
      };
      
      res.status(200).json(mockResponse);
    }
  } catch (error) {
    console.error('Chat API error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}