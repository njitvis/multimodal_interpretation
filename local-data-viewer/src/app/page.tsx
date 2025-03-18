'use client';

import React from 'react';
import Link from 'next/link'

const Home = () => {
  return (
    <ul>
      <li>
        <Link href="/browser">Extracted charts</Link>
      </li>
      <li>
        <Link href="/analysis">Visualize feature impact</Link>
      </li>
    </ul>
  );
}

export default Home;
