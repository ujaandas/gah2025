"use client";

import { useEffect } from 'react';

export function HydrationHandler() {
  useEffect(() => {
    // Remove loading class after hydration to enable transitions
    document.body.classList.remove('loading');
  }, []);

  return null;
}

