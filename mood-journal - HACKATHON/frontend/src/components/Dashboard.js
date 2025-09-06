import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MoodEntryForm from './MoodEntryForm';
import MoodEntryList from './MoodEntryList';

function Dashboard() {
  const [moodEntries, setMoodEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMoodEntries();
  }, []);

  const fetchMoodEntries = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/mood/entries');
      setMoodEntries(response.data.entries);
      setError('');
    } catch (error) {
      setError('Failed to fetch mood entries');
      console.error('Error fetching mood entries:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddMoodEntry = async (newEntry) => {
    try {
      const response = await axios.post('/mood/entries', newEntry);
      setMoodEntries([response.data.entry, ...moodEntries]);
      setError('');
    } catch (error) {
      setError('Failed to add mood entry');
      console.error('Error adding mood entry:', error);
    }
  };

  const handleDeleteMoodEntry = async (entryId) => {
    try {
      await axios.delete(`/mood/entries/${entryId}`);
      setMoodEntries(moodEntries.filter(entry => entry.id !== entryId));
      setError('');
    } catch (error) {
      setError('Failed to delete mood entry');
      console.error('Error deleting mood entry:', error);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Your Mood Dashboard</h1>
        <p className="mt-2 text-gray-600">Track your daily moods and emotions</p>
      </div>

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Mood Entry Form */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Add New Mood Entry</h2>
            <MoodEntryForm onAddMoodEntry={handleAddMoodEntry} />
          </div>
        </div>

        {/* Mood Entries List */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Your Mood History</h2>
            {loading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              </div>
            ) : (
              <MoodEntryList 
                entries={moodEntries} 
                onDeleteEntry={handleDeleteMoodEntry}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
