import React from 'react';
import Link from 'next/link';
import { FiHome, FiUsers, FiSettings, FiMenu, FiX } from 'react-icons/fi';

interface SidebarProps {
  isCollapsed: boolean;
  setIsCollapsed: (collapsed: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isCollapsed, setIsCollapsed }) => {
  const navItems = [
    { href: '/', icon: FiHome, label: 'Home' },
    { href: '/agents', icon: FiUsers, label: 'Agents' },
    { href: '/chat', icon: FiUsers, label: 'Chat' },
    { href: '/settings', icon: FiSettings, label: 'Settings' },
  ];

  return (
    <div className={`sidebar ${isCollapsed ? 'sidebar-collapsed' : 'sidebar-expanded'}`}>
      <div style={{ padding: '1rem' }}>
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--text)',
            cursor: 'pointer',
            padding: '0.5rem',
            borderRadius: '4px',
            width: '100%',
            display: 'flex',
            justifyContent: isCollapsed ? 'center' : 'flex-end',
          }}
        >
          {isCollapsed ? <FiMenu size={20} /> : <FiX size={20} />}
        </button>
      </div>
      
      <nav style={{ padding: '0 1rem' }}>
        {navItems.map((item) => (
          <Link key={item.href} href={item.href}>
            <div className="nav-item">
              <item.icon className="nav-icon" size={20} />
              {!isCollapsed && <span className="nav-text">{item.label}</span>}
            </div>
          </Link>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;