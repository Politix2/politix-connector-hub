
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Index from "./pages/Index";
import Dashboard from "./pages/Dashboard";
import SimpleDashboard from "./pages/SimpleDashboard";
import NotFound from "./pages/NotFound";
import { useEffect, useState } from "react";

const queryClient = new QueryClient();

const App = () => {
  const [setupComplete, setSetupComplete] = useState(false);
  
  useEffect(() => {
    // Check if user has completed setup
    const savedTopics = localStorage.getItem("userTopics");
    if (savedTopics) {
      setSetupComplete(true);
    }
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={setupComplete ? <Navigate to="/dashboard" /> : <Index />} />
            <Route path="/dashboard" element={<SimpleDashboard />} />
            <Route path="/dashboard/detailed" element={<Dashboard />} />
            <Route path="/topics" element={<SimpleDashboard />} />
            <Route path="/alerts" element={<SimpleDashboard />} />
            <Route path="/engagement" element={<SimpleDashboard />} />
            {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;
