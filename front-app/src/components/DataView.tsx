import React, { useState } from 'react'
import { motion } from 'framer-motion'

// Types for the data structure
interface Patient {
  name?: string;
  gender?: string;
  age?: string;
  age_group?: string;
  birthDate?: string;
  city?: string;
  state?: string;
  condition?: string;
}

interface Summary {
  total_patients?: number;
  gender_distribution?: { [key: string]: number };
  age_distribution?: { [key: string]: number };
  locations?: {
    cities?: { [key: string]: number };
    states?: { [key: string]: number };
  };
  [key: string]: number | { [key: string]: number } | string | { cities?: { [key: string]: number }; states?: { [key: string]: number } } | undefined;
}

interface DataViewProps {
  data: {
    results?: {
      params?: { [key: string]: string | number };
      patients?: Patient[];
      summary?: Summary;
    };
    [key: string]: unknown;
  };
}

type ViewType = 'table' | 'statistics' | 'gender-chart' | 'age-chart';

export default function DataView({ data }: DataViewProps) {
    const [activeView, setActiveView] = useState<ViewType>('table');
    const parsedData = data;
    console.log('DataView received data:', !parsedData);
    if (!parsedData || !parsedData.results) {
    return <div>No data available</div>;
  }
  const { results } = parsedData;
  const { summary, patients } = results;
  
  // View options for the sidebar
  const viewOptions = [
    { id: 'table', name: 'Patient Table', icon: '📋' },
    { id: 'statistics', name: 'Statistics', icon: '📊' },
    { id: 'gender-chart', name: 'Gender Chart', icon: '🥧' },
    { id: 'age-chart', name: 'Age Groups', icon: '📈' },
  ];

  // Render Patient Table
  const renderPatientTable = () => (
    <div className="h-full">
      <div className="overflow-auto max-h-full">
        <table className="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg">
          <thead className="bg-gray-50 dark:bg-gray-700 sticky top-0 z-10">
            <tr>
              {patients && patients.length > 0 && Object.keys(patients[0]).map((key) => (
                <th key={key} className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider border-b border-gray-200 dark:border-gray-600">
                  {key.replace(/(_)/g, ' ').replace(/^./, str => str.toUpperCase())}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {patients && patients.map((patient: Patient, index: number) => (
              <tr key={index} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                {Object.values(patient).map((value, cellIndex) => (
                  <td key={cellIndex} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100 border-b border-gray-100 dark:border-gray-600">
                    {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {(!patients || patients.length === 0) && (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            No patient data available
          </div>
        )}
      </div>
    </div>
  );

  // Render Statistics
  const renderStatistics = () => (
    <div className="space-y-8">
      {/* Main Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {summary && Object.entries(summary).map(([key, value]) => {
          // Skip locations as we'll handle it separately
          if (key === 'locations') return null;
          
          return (
            <div key={key} className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                {key.replace(/(_)/g, ' ').replace(/^./, str => str.toUpperCase())}
              </h3>
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {typeof value === 'object' && value !== null ? (
                  <div className="text-sm font-normal space-y-1">
                    {Object.entries(value).map(([subKey, subValue]) => (
                      <div key={subKey} className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">{subKey}:</span>
                        <span className="font-semibold">{String(subValue)}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  String(value)
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Locations Section */}
      {summary?.locations && (
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Location Distribution</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Cities */}
            {summary.locations.cities && (
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Cities</h3>
                <div className="space-y-2 max-h-60 overflow-y-auto">
                  {Object.entries(summary.locations.cities)
                    .sort(([,a], [,b]) => (b as number) - (a as number))
                    .map(([city, count]) => (
                      <div key={city} className="flex justify-between items-center">
                        <span className="text-sm text-gray-700 dark:text-gray-300">{city}</span>
                        <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">{String(count)}</span>
                      </div>
                    ))}
                </div>
              </div>
            )}

            {/* States */}
            {summary.locations.states && (
              <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">States</h3>
                <div className="space-y-2 max-h-60 overflow-y-auto">
                  {Object.entries(summary.locations.states)
                    .sort(([,a], [,b]) => (b as number) - (a as number))
                    .map(([state, count]) => (
                      <div key={state} className="flex justify-between items-center">
                        <span className="text-sm text-gray-700 dark:text-gray-300">{state}</span>
                        <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">{String(count)}</span>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );

  // Render Gender Pie Chart
  const renderGenderChart = () => {
    const genderData = summary?.gender_distribution || {};
    const total = Object.values(genderData).reduce((acc: number, val) => acc + (val as number), 0);
    
    if (total === 0) {
      return <div className="text-center py-8 text-gray-500 dark:text-gray-400">No gender data available</div>;
    }

    const colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6'];
    let cumulativePercentage = 0;

    return (
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-6">Gender Distribution</h3>
        <div className="flex items-center justify-center">
          <div className="relative w-64 h-64">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              {Object.entries(genderData).map(([gender, count], index) => {
                const percentage = (count as number) / total;
                const strokeDasharray = `${percentage * 100} ${100 - (percentage * 100)}`;
                const strokeDashoffset = -cumulativePercentage * 100;
                cumulativePercentage += percentage;
                
                return (
                  <circle
                    key={gender}
                    cx="50"
                    cy="50"
                    r="15.915"
                    fill="transparent"
                    stroke={colors[index % colors.length]}
                    strokeWidth="4"
                    strokeDasharray={strokeDasharray}
                    strokeDashoffset={strokeDashoffset}
                    className="opacity-80 hover:opacity-100 transition-opacity"
                  />
                );
              })}
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">{total}</div>
                <div className="text-sm text-gray-500 dark:text-gray-400">Total</div>
              </div>
            </div>
          </div>
        </div>
        <div className="mt-6 grid grid-cols-2 gap-4">
          {Object.entries(genderData).map(([gender, count], index) => (
            <div key={gender} className="flex items-center">
              <div
                className="w-4 h-4 rounded-full mr-3"
                style={{ backgroundColor: colors[index % colors.length] }}
              ></div>
              <span className="text-sm text-gray-700 dark:text-gray-300">
                {gender}: {String(count)} ({Math.round(((count as number) / total) * 100)}%)
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // Render Age Groups Bar Chart
  const renderAgeChart = () => {
    const ageData = summary?.age_distribution || {};
    const maxValue = Math.max(...Object.values(ageData).map(val => val as number));
    
    if (maxValue === 0) {
      return <div className="text-center py-8 text-gray-500 dark:text-gray-400">No age group data available</div>;
    }

    return (
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-6">Age Group Distribution</h3>
        <div className="space-y-4">
          {Object.entries(ageData).map(([ageGroup, count]) => (
            <div key={ageGroup} className="flex items-center">
              <div className="w-20 text-sm font-medium text-gray-700 dark:text-gray-300 mr-4">
                {ageGroup}
              </div>
              <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-6 relative overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-end pr-2"
                  initial={{ width: 0 }}
                  animate={{ width: `${((count as number) / maxValue) * 100}%` }}
                  transition={{ duration: 1, ease: "easeOut" }}
                >
                  <span className="text-white text-xs font-medium">{String(count)}</span>
                </motion.div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderContent = () => {
    switch (activeView) {
      case 'table':
        return renderPatientTable();
      case 'statistics':
        return renderStatistics();
      case 'gender-chart':
        return renderGenderChart();
      case 'age-chart':
        return renderAgeChart();
      default:
        return renderPatientTable();
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto h-[400px] bg-gray-50 dark:bg-gray-900 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700 shadow-lg flex">
      {/* Sidebar */}
      <div className="w-48 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex-shrink-0">
        <div className="p-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Data Views</h2>
          <nav className="space-y-2">
            {viewOptions.map((option) => (
              <button
                key={option.id}
                onClick={() => setActiveView(option.id as ViewType)}
                className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                  activeView === option.id
                    ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-200'
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <span className="mr-3">{option.icon}</span>
                {option.name}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content - Fixed height with internal scrolling */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full overflow-auto p-6">
          <motion.div
            key={activeView}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="min-h-full"
          >
            {renderContent()}
          </motion.div>
        </div>
      </div>
    </div>
  )
}
