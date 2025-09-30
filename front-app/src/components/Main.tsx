import React from 'react'

export default function Main({ generations, handleQuickPrompt }: { generations: Array<{ id: number; content: string; timestamp: Date }>, handleQuickPrompt: (promptText: string) => void }) {
    
  return (
    <main className="flex-1 overflow-y-auto px-4 py-6">
            {/* Main Generation Area - Scrollable */}
        <div className="max-w-4xl mx-auto">
          {generations.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <h1 className="text-5xl font-bold mb-4 text-gray-200">
                Welcome to MediFire
              </h1>
              <p className="text-lg text-gray-400 mb-8 max-w-2xl">
                Start prompting to extract insights, and visualize data from FHIR resources.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-3xl">
                <button 
                  onClick={() => handleQuickPrompt("Find all patients with diabetes who are males")}
                  className="p-4 rounded-lg border border-gray-700 bg-gray-800/50 hover:bg-gray-700/50 transition-colors cursor-pointer text-left"
                >
                  <h3 className="font-semibold mb-2">Find Patients</h3>
                  <p className="text-sm text-gray-400">Find all patients with diabetes who are males</p>
                </button>
                <button 
                  onClick={() => handleQuickPrompt("Create a new patient entry for a 45-year-old male named John Doe")}
                  className="p-4 rounded-lg border border-gray-700 bg-gray-800/50 hover:bg-gray-700/50 transition-colors cursor-pointer text-left"
                >
                  <h3 className="font-semibold mb-2">Create New Entries</h3>
                  <p className="text-sm text-gray-400">Add a new patient, 45-year-old male named John Doe</p>
                </button>
                <button 
                  onClick={() => handleQuickPrompt("Show me patients over 60 with hypertension")}
                  className="p-4 rounded-lg border border-gray-700 bg-gray-800/50 hover:bg-gray-700/50 transition-colors cursor-pointer text-left"
                >
                  <h3 className="font-semibold mb-2">Search for Insights</h3>
                  <p className="text-sm text-gray-400">Show me patients over 60 with hypertension</p>
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {generations.map((generation) => (
                <div key={generation.id} className="bg-gray-800 rounded-lg shadow-sm border border-gray-700 p-6">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="font-semibold text-gray-200">Generated Content</h3>
                    <span className="text-sm text-gray-400">
                      {generation.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                  <div className="mb-4 p-4 bg-gray-900 rounded-md">
                    <p className="text-sm text-gray-400 mb-2">Prompt:</p>
                    <p className="font-medium">{generation.content}</p>
                  </div>
                  <div className="p-4 bg-blue-900/20 rounded-md">
                    <p className="text-sm text-gray-400 mb-2">Generated Response:</p>
                    <p>This is where your AI-generated content would appear based on the prompt: &quot;{generation.content}&quot;</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
    </main>
  )
}
