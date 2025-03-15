
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-sm py-4 px-6 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link to="/" className="flex items-center space-x-2">
          <div className="flex items-center">
            <span className="text-politix-blue font-bold text-2xl">Politi</span>
            <span className="text-politix-red font-bold text-2xl">X</span>
          </div>
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
