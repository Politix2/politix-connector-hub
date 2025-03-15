
import { Link } from "react-router-dom";

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-politix-dark text-white py-12 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="col-span-1 md:col-span-1">
            <Link to="/" className="flex items-center mb-4">
              <div className="flex items-center">
                <span className="text-white font-bold text-2xl">Politi</span>
                <span className="text-politix-red font-bold text-2xl">X</span>
              </div>
            </Link>
            <p className="text-gray-400 mb-4">
              Making political data accessible and understandable for everyone.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Platform</h3>
            <ul className="space-y-2">
              <li><Link to="/" className="text-gray-400 hover:text-white transition-colors">Home</Link></li>
              <li><Link to="/dashboard" className="text-gray-400 hover:text-white transition-colors">Dashboard</Link></li>
              <li><Link to="#features" className="text-gray-400 hover:text-white transition-colors">Features</Link></li>
              <li><Link to="#about" className="text-gray-400 hover:text-white transition-colors">About</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">About Us</Link></li>
              <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Careers</Link></li>
              <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Privacy Policy</Link></li>
              <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Terms of Service</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Connect</h3>
            <ul className="space-y-2">
              <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Twitter</Link></li>
              <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">LinkedIn</Link></li>
              <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Facebook</Link></li>
              <li><Link to="#" className="text-gray-400 hover:text-white transition-colors">Contact Us</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 pt-8">
          <p className="text-center text-gray-500">
            © {currentYear} PolitiX. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
