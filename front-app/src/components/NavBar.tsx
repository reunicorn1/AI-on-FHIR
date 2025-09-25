import React from 'react'
import Image from 'next/image';

export default function NavBar() {
  return (
      <nav className="flex w-full items-center justify-between border-t border-b border-neutral-200 px-6 py-2 dark:border-neutral-800">
            <Image
              src="/medifire.svg"
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
                  className="dark:invert"
                  src="/github-3.png"
                  alt="GitHub Logo"
                  width={25}
                  height={25}
                />
              </a>
            </nav>
      </nav>
    );
}
