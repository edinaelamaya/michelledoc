import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import {Navbar} from '../Navbar/Navbar';
import {Sidebar} from '../Sidebar/Sidebar';
import {VoiceIndicator} from '../VoiceIndicator/VoiceIndicator';
import './Layout.styles.css';

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="app-container">
      <Navbar onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />
      
      <div className="content-wrapper">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        
        <main className="main-content">
          <Outlet />
          <VoiceIndicator />
        </main>
      </div>
    </div>
  );
}