
import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Features from "@/components/Features";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { CheckCircle2 } from "lucide-react";

const Index = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-grow">
        <Hero />
        <Features />
        
        {/* About Section */}
        <section id="about" className="py-20 px-6">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4 text-politix-dark">About PolitiX</h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                We're on a mission to make political data accessible, understandable, and actionable for everyone.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
              <div>
                <h3 className="text-2xl font-bold mb-4 text-politix-blue">Our Mission</h3>
                <p className="text-gray-600 mb-6">
                  PolitiX was founded on the belief that informed citizens make better choices. We strive to cut through the political noise and provide data-driven insights that help people understand the complex political landscape.
                </p>
                
                <h3 className="text-2xl font-bold mb-4 text-politix-blue">Our Approach</h3>
                <p className="text-gray-600 mb-6">
                  We combine advanced data visualization with rigorous analysis to present political information in an accessible format. Our platform is designed to be non-partisan, focusing on facts rather than opinions.
                </p>
                
                <Button className="bg-politix-blue hover:bg-politix-dark">
                  Learn More About Us
                </Button>
              </div>
              
              <div>
                <Card className="border-0 shadow-lg">
                  <CardContent className="p-8">
                    <h3 className="text-2xl font-bold mb-6 text-center">Why Choose PolitiX?</h3>
                    
                    <div className="space-y-4">
                      <div className="flex items-start">
                        <CheckCircle2 className="h-6 w-6 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                        <div>
                          <h4 className="font-semibold text-lg">Data-Driven Analysis</h4>
                          <p className="text-gray-600">We rely on verified data sources and rigorous methodologies.</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start">
                        <CheckCircle2 className="h-6 w-6 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                        <div>
                          <h4 className="font-semibold text-lg">Political Neutrality</h4>
                          <p className="text-gray-600">We present facts without partisan bias or agenda.</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start">
                        <CheckCircle2 className="h-6 w-6 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                        <div>
                          <h4 className="font-semibold text-lg">Intuitive Visualizations</h4>
                          <p className="text-gray-600">Complex data presented in easy-to-understand formats.</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start">
                        <CheckCircle2 className="h-6 w-6 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                        <div>
                          <h4 className="font-semibold text-lg">Real-Time Updates</h4>
                          <p className="text-gray-600">Stay current with the latest political developments.</p>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </section>
        
        {/* CTA Section */}
        <section className="py-20 px-6 bg-gradient-to-r from-politix-blue to-politix-dark text-white">
          <div className="max-w-7xl mx-auto text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Ready to Explore Political Data?</h2>
            <p className="text-xl mb-8 max-w-2xl mx-auto">
              Start using PolitiX today and gain valuable insights into the political landscape.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Button className="bg-white text-politix-blue hover:bg-gray-100 text-lg px-8 py-6">
                Get Started
              </Button>
              <Button variant="outline" className="border-white text-white hover:bg-white/10 text-lg px-8 py-6">
                Schedule a Demo
              </Button>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default Index;
