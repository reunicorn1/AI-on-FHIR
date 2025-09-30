"use client";

import { motion } from "motion/react";
import { useEffect, useRef } from "react";
import DataView from "./DataView";

// Types to match the new Generation interface
interface Generation {
  id: number;
  userPrompt: string;
  aiResponse?: string;
  timestamp: Date;
  isLoading?: boolean;
  error?: string;
}

export default function HeroSectionOne({ 
  generations, 
  handleQuickPrompt 
}: { 
  generations: Generation[], 
  handleQuickPrompt: (promptText: string) => void 
}) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new content is added (like a chat)
  useEffect(() => {
    if (generations.length > 0 && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [generations]);

  return (
    <div className="h-full flex items-center justify-center p-4">
      {/* Fixed bordered container */}
      <div className="relative max-w-5xl w-full h-full">
        {/* Fixed borders - never scroll */}
        <div className="absolute inset-y-0 left-0 h-full w-px bg-neutral-800/80">
          <div className="absolute top-0 h-40 w-px bg-gradient-to-b from-transparent via-orange-500 to-transparent" />
        </div>
        <div className="absolute inset-y-0 right-0 h-full w-px bg-neutral-800/80">
          <div className="absolute h-40 w-px bg-gradient-to-b from-transparent via-orange-500 to-transparent" />
        </div>
        <div className="absolute inset-x-0 bottom-0 h-px w-full bg-neutral-800/80">
          <div className="absolute mx-auto h-px w-40 bg-gradient-to-r from-transparent via-orange-500 to-transparent" />
        </div>
        
        {generations.length === 0 ? (
          /* Empty state - centered hero content */
          <div className="h-full flex items-center justify-center px-8">
            <div className="py-10 md:py-17 w-full text-center">
        <h1 className="relative z-10 mx-auto max-w-4xl text-center text-2xl font-bold text-white md:text-4xl lg:text-7xl">
          {"Where Your Health Data Sparks Smarter Care"
            .split(" ")
            .map((word, index) => (
              <motion.span
                key={index}
                initial={{ opacity: 0, filter: "blur(4px)", y: 10 }}
                animate={{ opacity: 1, filter: "blur(0px)", y: 0 }}
                transition={{
                  duration: 0.3,
                  delay: index * 0.1,
                  ease: "easeInOut",
                }}
                className="mr-2 inline-block"
              >
                {word}
              </motion.span>
            ))}
        </h1>
        <motion.p
          initial={{
            opacity: 0,
          }}
          animate={{
            opacity: 1,
          }}
          transition={{
            duration: 0.3,
            delay: 0.8,
          }}
          className="relative z-10 mx-auto max-w-xl py-4 text-center text-lg font-normal text-neutral-400"
        >
          MediFire connects patient responses with your FHIR data to deliver instant, actionable insights.
        </motion.p>
        <motion.div
          initial={{
            opacity: 0,
          }}
          animate={{
            opacity: 1,
          }}
          transition={{
            duration: 0.3,
            delay: 1,
          }}
          className="relative z-10 mt-8 flex flex-wrap items-center justify-center gap-4"
        >
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-3xl">
                <button 
                  onClick={() => handleQuickPrompt && handleQuickPrompt("Find all patients with diabetes who are males")}
                  className="p-4 rounded-lg border border-gray-800 text-black bg-gray-100 hover:bg-gray-300 transition-colors cursor-pointer text-left"
                >
                  <h3 className="font-semibold mb-2">Find Patients</h3>
                  <p className="text-sm text-gray-400">Find all patients with diabetes who are males</p>
                </button>
                <button 
                  onClick={() => handleQuickPrompt && handleQuickPrompt("Create a new patient entry for a 45-year-old male named John Doe")}
                  className="p-4 rounded-lg border border-gray-700 bg-gray-800/50 hover:bg-gray-700/50 transition-colors cursor-pointer text-left"
                >
                  <h3 className="font-semibold mb-2">Create New Entries</h3>
                  <p className="text-sm text-gray-400">Add a new patient, 45-year-old male named John Doe</p>
                </button>
                <button 
                  onClick={() => handleQuickPrompt && handleQuickPrompt("Show me patients over 60 with hypertension")}
                  className="p-4 rounded-lg border border-gray-700 bg-gray-800/50hover:bg-gray-700/50 transition-colors cursor-pointer text-left"
                >
                  <h3 className="font-semibold mb-2">Search for Insights</h3>
                  <p className="text-sm text-gray-400">Show me patients over 60 with hypertension</p>
                </button>
              </div>
            </motion.div>
          </div>
        </div>
        ) : (
          /* Chat mode - scrollable content with messages at bottom */
          <motion.div 
            ref={scrollRef} 
            className="h-full overflow-y-auto px-8 flex flex-col"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, ease: "easeInOut" }}
          >
            {/* Spacer to push content to bottom initially */}
            <div className="flex-1"></div>
            
            {/* Chat messages - newest at bottom */}
            <div className="space-y-6 py-6">
              {generations.map((generation, index) => (
                <motion.div 
                  key={generation.id} 
                  className="bg-neutral-800 rounded-lg shadow-sm border border-gray-700 p-6"
                  initial={{ opacity: 0, y: 20, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ 
                    duration: 0.4, 
                    delay: index * 0.1, 
                    ease: "easeOut",
                    type: "spring",
                    stiffness: 100,
                    damping: 15
                  }}
                >
                  <motion.div 
                    className="flex items-start justify-between mb-4"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.3, delay: (index * 0.1) + 0.2 }}
                  >
                    <span className="text-sm text-gray-400">
                      {generation.timestamp.toLocaleTimeString()}
                    </span>
                  </motion.div>
                  <motion.div 
                    className="mb-4 p-4 bg-neutral-900 rounded-md"
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: (index * 0.1) + 0.3 }}
                  >
                    <p className="text-sm text-gray-400 mb-2">User:</p>
                    <p className="font-medium">{generation.userPrompt}</p>
                  </motion.div>
                  <motion.div 
                    className="p-4 bg-zinc-700 rounded-md"
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: (index * 0.1) + 0.4 }}
                  >
                    <p className="text-sm text-gray-400 mb-2">AI Assistant:</p>
                    {generation.isLoading ? (
                      // Loading state - you can customize this component
                      <div className="flex items-center gap-3">
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-500 border-t-transparent"></div>
                        <p className="text-gray-500">Generating response...</p>
                      </div>
                    ) : generation.error ? (
                      // Error state
                      <div className="flex items-center gap-2 text-red-400">
                        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p>{generation.error}</p>
                      </div>
                    ) : (
                      // Success state with AI response
                      <DataView data={ JSON.parse(generation.aiResponse ?? '{}') } />
                    )}
                  </motion.div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
