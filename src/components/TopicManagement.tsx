
import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Plus, Info, Edit, Save, X } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

interface Topic {
  name: string;
  description: string;
}

interface TopicManagementProps {
  topics: Topic[];
  onUpdateTopics: (topics: Topic[]) => void;
}

const TopicManagement = ({ topics, onUpdateTopics }: TopicManagementProps) => {
  const [editingTopicIndex, setEditingTopicIndex] = useState<number | null>(null);
  const [topicDescription, setTopicDescription] = useState("");
  const [newTopicName, setNewTopicName] = useState("");
  const [newTopicDescription, setNewTopicDescription] = useState("");
  const { toast } = useToast();

  const handleSaveDescription = (index: number) => {
    const updatedTopics = [...topics];
    updatedTopics[index] = {
      ...updatedTopics[index],
      description: topicDescription
    };
    onUpdateTopics(updatedTopics);
    setEditingTopicIndex(null);
    
    toast({
      title: "Topic updated",
      description: `Description for "${topics[index].name}" has been updated.`,
    });
  };

  const handleAddTopic = () => {
    if (!newTopicName.trim()) {
      toast({
        title: "Error",
        description: "Topic name cannot be empty",
        variant: "destructive",
      });
      return;
    }
    
    // Check if topic already exists
    if (topics.some(topic => topic.name.toLowerCase() === newTopicName.toLowerCase())) {
      toast({
        title: "Error",
        description: "This topic already exists",
        variant: "destructive",
      });
      return;
    }
    
    const updatedTopics = [
      ...topics,
      { name: newTopicName, description: newTopicDescription }
    ];
    onUpdateTopics(updatedTopics);
    
    // Reset form
    setNewTopicName("");
    setNewTopicDescription("");
    
    toast({
      title: "Topic added",
      description: `"${newTopicName}" has been added to your monitored topics.`,
    });
  };

  const startEditing = (index: number) => {
    setEditingTopicIndex(index);
    setTopicDescription(topics[index].description || "");
  };

  const cancelEditing = () => {
    setEditingTopicIndex(null);
  };

  return (
    <div className="mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Monitored Topics</h2>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline" className="flex items-center gap-2">
              <Plus className="h-4 w-4" />
              Add New Topic
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add New Topic</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="topic-name">Topic Name</Label>
                <Input
                  id="topic-name"
                  placeholder="e.g., Carbon Pricing"
                  value={newTopicName}
                  onChange={(e) => setNewTopicName(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="topic-description">Description (Optional)</Label>
                <Textarea
                  id="topic-description"
                  placeholder="Describe what specific aspects of this topic you want to monitor..."
                  value={newTopicDescription}
                  onChange={(e) => setNewTopicDescription(e.target.value)}
                  rows={4}
                />
              </div>
              <Button className="w-full" onClick={handleAddTopic}>
                Add Topic
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {topics.map((topic, index) => (
          <Card key={index} className="w-full">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg flex justify-between items-center">
                <span>{topic.name}</span>
                {editingTopicIndex !== index && (
                  <Button variant="ghost" size="sm" onClick={() => startEditing(index)}>
                    <Info className="h-4 w-4" />
                  </Button>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {editingTopicIndex === index ? (
                <Textarea
                  value={topicDescription}
                  onChange={(e) => setTopicDescription(e.target.value)}
                  placeholder="Describe what specific aspects of this topic you want to monitor..."
                  rows={3}
                />
              ) : (
                <p className="text-sm text-muted-foreground">
                  {topic.description || "Click the info icon to add a detailed description of this topic."}
                </p>
              )}
            </CardContent>
            {editingTopicIndex === index && (
              <CardFooter className="border-t pt-3 flex justify-end gap-2">
                <Button variant="ghost" size="sm" onClick={cancelEditing}>
                  <X className="h-4 w-4 mr-1" /> Cancel
                </Button>
                <Button size="sm" onClick={() => handleSaveDescription(index)}>
                  <Save className="h-4 w-4 mr-1" /> Save
                </Button>
              </CardFooter>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
};

export default TopicManagement;
