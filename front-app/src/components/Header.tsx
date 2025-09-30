'use client';
import React from 'react';
import Image from 'next/image';

const Header = () => {
  return (
    <>
      {/* Header */}
      <header className="flex-shrink-0 p-4 border-b border-gray-800">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <Image
            src="/medifire.png"
            alt="Medifire Logo"
            width={140}
            height={45}
            priority
          />
          <nav className="flex gap-4">
            <a 
              href="https://github.com/reunicorn1/AI-on-FHIR" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-sm transition-transform duration-200 hover:scale-95 active:scale-90 inline-block"
            >
              <Image 
                className="invert"
                src="/github-3.png"
                alt="GitHub Logo"
                width={25}
                height={25}
              />
            </a>
          </nav>
        </div>
      </header>
    </>
  );
}
export default Header;