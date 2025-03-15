
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Menu, X, BarChart2, PieChart, Globe } from 'lucide-react';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  return (
    <nav className="bg-white shadow-sm py-4 px-6 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link to="/" className="flex items-center space-x-2">
          <div className="flex items-center">
            <span className="text-politix-blue font-bold text-2xl">Politi</span>
            <span className="text-politix-red font-bold text-2xl">X</span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center space-x-6">
          <Link to="/" className="text-gray-700 hover:text-politix-blue font-medium transition-colors">
            Home
          </Link>
          <Link to="/dashboard" className="text-gray-700 hover:text-politix-blue font-medium transition-colors">
            Dashboard
          </Link>
          <Link to="#features" className="text-gray-700 hover:text-politix-blue font-medium transition-colors">
            Features
          </Link>
          <Link to="#about" className="text-gray-700 hover:text-politix-blue font-medium transition-colors">
            About
          </Link>
          <Button variant="default" className="bg-politix-blue hover:bg-politix-dark text-white">
            Get Started
          </Button>
        </div>

        {/* Mobile Menu Button */}
        <div className="md:hidden">
          <Button variant="ghost" onClick={toggleMenu} className="p-1">
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </Button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden mt-4 px-6 pb-4 pt-2 bg-white animate-fade-in">
          <div className="flex flex-col space-y-4">
            <Link 
              to="/" 
              className="text-gray-700 hover:text-politix-blue font-medium py-2 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Home
            </Link>
            <Link 
              to="/dashboard" 
              className="text-gray-700 hover:text-politix-blue font-medium py-2 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Dashboard
            </Link>
            <Link 
              to="#features" 
              className="text-gray-700 hover:text-politix-blue font-medium py-2 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Features
            </Link>
            <Link 
              to="#about" 
              className="text-gray-700 hover:text-politix-blue font-medium py-2 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              About
            </Link>
            <Button 
              variant="default" 
              className="bg-politix-blue hover:bg-politix-dark text-white w-full"
              onClick={() => setIsMenuOpen(false)}
            >
              Get Started
            </Button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
