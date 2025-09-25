import { Geist, Geist_Mono } from "next/font/google";
import { useState } from "react";
import Bottom from "@/components/Bottom";
import NavBar from "@/components/NavBar";
import HeroSectionOne from "@/components/hero-section-demo-1";
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL

type FHIRResponse = {
  response?: string;
  error?: string;
};
// Types for better type safety
interface Generation {
  id: number;
  userPrompt: string;
  aiResponse?: string;
  timestamp: Date;
  isLoading?: boolean;
  error?: string;
}

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [generations, setGenerations] = useState<Generation[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  // Simple API call with POST request and JSON body - just replace the endpoint URL
  const callGenerateAPI = async (userPrompt: string): Promise<FHIRResponse> => {
    const API_ENDPOINT = '/query'; // Replace with your endpoint

    const response = await fetch(`${BACKEND_URL}${API_ENDPOINT}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',

      },
      body: JSON.stringify({
        query: userPrompt,
      }),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    
    // Adjust this based on your API response structure
    return {
      response: data.response || data.result || data.answer || JSON.stringify(data),
      error: data.error
    };
  };

  const handleGenerate = async () => {
    if (prompt.trim() && !isGenerating) {
      const generationId = Date.now();
      const userPrompt = prompt.trim();
      
      // Clear the input immediately
      setPrompt("");
      setIsGenerating(true);

      // Add the generation with loading state
      const newGeneration: Generation = {
        id: generationId,
        userPrompt,
        timestamp: new Date(),
        isLoading: true,
      };
      
      setGenerations(prev => [...prev, newGeneration]);

      try {
        // Call your API
        const apiResponse = await callGenerateAPI(userPrompt);
        
        // Update the generation with the response
        setGenerations(prev => 
          prev.map(gen => 
            gen.id === generationId 
              ? { ...gen, aiResponse: apiResponse.response || 'No response received', isLoading: false }
              : gen
          )
        );
      } catch (error) {
        // Handle API errors
        const errorMessage = error instanceof Error ? error.message : 'Failed to generate response';
        
        setGenerations(prev => 
          prev.map(gen => 
            gen.id === generationId 
              ? { ...gen, error: errorMessage, isLoading: false }
              : gen
          )
        );
      } finally {
        setIsGenerating(false);
      }
    }
  };

  const handleQuickPrompt = async (promptText: string) => {
    setPrompt(promptText);
    
    // Trigger generation with the quick prompt
    if (!isGenerating) {
      const generationId = Date.now();
      
      setIsGenerating(true);
      
      // Add the generation with loading state
      const newGeneration: Generation = {
        id: generationId,
        userPrompt: promptText,
        timestamp: new Date(),
        isLoading: true,
      };
      
      setGenerations(prev => [...prev, newGeneration]);
      setPrompt(""); // Clear prompt after adding to generations

      try {
        // Call your API
        const apiResponse = await callGenerateAPI(promptText);
        
        // Update the generation with the response
        setGenerations(prev => 
          prev.map(gen => 
            gen.id === generationId 
              ? { ...gen, aiResponse: apiResponse.response || 'No response received', isLoading: false }
              : gen
          )
        );
      } catch (error) {
        // Handle API errors
        const errorMessage = error instanceof Error ? error.message : 'Failed to generate response';
        
        setGenerations(prev => 
          prev.map(gen => 
            gen.id === generationId 
              ? { ...gen, error: errorMessage, isLoading: false }
              : gen
          )
        );
      } finally {
        setIsGenerating(false);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleGenerate();
    }
  };

  return (
    <div className={`${geistSans.variable} ${geistMono.variable} h-screen flex flex-col text-foreground`}>
      {/* NavBar at top */}
      <NavBar />
      
      {/* Hero Section fills remaining space */}
      <div className="flex-1 overflow-auto">
        <HeroSectionOne generations={generations} handleQuickPrompt={handleQuickPrompt} />
      </div>
      
      {/* Bottom fixed at bottom */}
      <Bottom
        prompt={prompt}
        setPrompt={setPrompt}
        handleGenerate={handleGenerate}
        handleKeyPress={handleKeyPress}
        isGenerating={isGenerating}
      />
    </div>
  );
}