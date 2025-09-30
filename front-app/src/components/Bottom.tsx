import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AUTO_COMPLETE_SUGGESTIONS } from "@/constants/autoCompleteSuggestions";


export default function Bottom({ 
  prompt, 
  setPrompt, 
  handleGenerate, 
  handleKeyPress, 
  isGenerating = false 
}: { 
  prompt: string; 
  setPrompt: (value: string) => void; 
  handleGenerate: () => void; 
  handleKeyPress: (e: React.KeyboardEvent) => void;
  isGenerating?: boolean;
}) {
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  // Filter suggestions based on input
  useEffect(() => {
    if (prompt.trim().length >= 2) {
      const filtered = AUTO_COMPLETE_SUGGESTIONS.filter(suggestion =>
        suggestion.toLowerCase().includes(prompt.toLowerCase())
      ).slice(0, 5); // Show max 5 suggestions
      
      setFilteredSuggestions(filtered);
      setShowSuggestions(filtered.length > 0);
      setSelectedIndex(-1);
    } else {
      setShowSuggestions(false);
      setFilteredSuggestions([]);
    }
  }, [prompt]);

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (showSuggestions && filteredSuggestions.length > 0) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(prev => 
          prev < filteredSuggestions.length - 1 ? prev + 1 : 0
        );
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(prev => 
          prev > 0 ? prev - 1 : filteredSuggestions.length - 1
        );
      } else if (e.key === 'Enter' && selectedIndex >= 0) {
        e.preventDefault();
        selectSuggestion(filteredSuggestions[selectedIndex]);
        return;
      } else if (e.key === 'Escape') {
        setShowSuggestions(false);
        setSelectedIndex(-1);
        return;
      }
    }
    
    // Handle original key press logic
    handleKeyPress(e);
  };

  const selectSuggestion = (suggestion: string) => {
    setPrompt(suggestion);
    setShowSuggestions(false);
    setSelectedIndex(-1);
    textareaRef.current?.focus();
  };

  return (
    <div className="flex-shrink-0 border-t border-zinc-800 bg-black p-2">
      <div className="max-w-5xl mx-auto px-4">
        <div className="relative">
          {/* Auto-complete suggestions dropdown */}
          <AnimatePresence>
            {showSuggestions && filteredSuggestions.length > 1 && (
              <motion.div
                ref={suggestionsRef}
                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                animate={{ opacity: 0.9, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 10, scale: 0.95 }}
                transition={{ duration: 0.15, ease: "easeOut" }}
                className="absolute bottom-full left-0 right-0 mb-2 bg-zinc-800 border-zinc-700 rounded-lg shadow-lg max-h-48 overflow-y-auto z-50"
              >
                <div className="py-1">
                  {filteredSuggestions.map((suggestion, index) => (
                    <motion.button
                      key={suggestion}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.1, delay: index * 0.02 }}
                      onClick={() => selectSuggestion(suggestion)}
                      className={`w-full text-left px-4 py-3 hover:bg-gray-700 border-b border-gray-700 last:border-b-0 transition-colors ${
                        index === selectedIndex ? 'bg-blue-900/20 border-blue-700' : ''
                      }`}
                    >
                      <div className="text-sm text-gray-100 font-medium">
                        {suggestion}
                      </div>
                    </motion.button>
                  ))}
                </div>
                <div className="px-4 py-2 border-t border-gray-700 bg-neutral-800/50">
                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <span>↑↓ Navigate • Enter Select • Esc Close</span>
                    <span>{filteredSuggestions.length} suggestions</span>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <textarea
            ref={textareaRef}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Query insights about FHIR... (Press Enter to generate, Shift+Enter for new line)"
            className="w-full p-3 pr-16 border border-gray-600 rounded-lg resize-none bg-neutral-900 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            rows={2}
            maxLength={1000}
          />
          <div className="absolute bottom-2 right-2 flex items-center gap-2">
            <span className="text-xs text-gray-400">
              {prompt.length}/1000
            </span>
            <button
              onClick={handleGenerate}
              disabled={!prompt.trim() || isGenerating}
              className="px-3 py-1.5 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-md text-xs font-medium transition-colors flex items-center gap-2"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-3 w-3 border-2 border-white border-t-transparent"></div>
                  <span>Generating...</span>
                </>
              ) : (
                "Generate"
              )}
            </button>
          </div>
        </div>
        <div className="flex justify-between items-center mt-1 text-xs text-gray-400">
          <div className="flex gap-3">
            <span>Press Enter to generate</span>
            <span>Shift+Enter for new line</span>
          </div>
          <div className="flex gap-2">
            <button className="hover:text-gray-300">Clear</button>
            <button className="hover:text-gray-300">Settings</button>
          </div>
        </div>
      </div>
    </div>
  )
}
