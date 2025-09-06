import React, { useState } from 'react';

function MoodEntryForm({ onAddMoodEntry }) {
  const [formData, setFormData] = useState({
    mood: '',
    date: new Date().toISOString().split('T')[0],
    notes: ''
  });
  const [loading, setLoading] = useState(false);

  const moodOptions = [
    { value: 'happy', label: '😊 Happy', color: 'bg-green-100 text-green-800' },
    { value: 'excited', label: '🤩 Excited', color: 'bg-yellow-100 text-yellow-800' },
    { value: 'calm', label: '😌 Calm', color: 'bg-blue-100 text-blue-800' },
    { value: 'sad', label: '😢 Sad', color: 'bg-gray-100 text-gray-800' },
    { value: 'anxious', label: '😰 Anxious', color: 'bg-orange-100 text-orange-800' },
    { value: 'angry', label: '😠 Angry', color: 'bg-red-100 text-red-800' },
    { value: 'tired', label: '😴 Tired', color: 'bg-purple-100 text-purple-800' },
    { value: 'confused', label: '😕 Confused', color: 'bg-indigo-100 text-indigo-800' }
  ];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.mood) return;

    setLoading(true);
    await onAddMoodEntry(formData);
    
    // Reset form
    setFormData({
      mood: '',
      date: new Date().toISOString().split('T')[0],
      notes: ''
    });
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Mood Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          How are you feeling today? *
        </label>
        <div className="grid grid-cols-2 gap-2">
          {moodOptions.map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => setFormData({ ...formData, mood: option.value })}
              className={`p-3 rounded-lg border-2 transition-all duration-200 text-sm font-medium ${
                formData.mood === option.value
                  ? `${option.color} border-primary-500 ring-2 ring-primary-200`
                  : 'bg-white border-gray-200 hover:border-gray-300 text-gray-700'
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* Date Selection */}
      <div>
        <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-1">
          Date
        </label>
        <input
          type="date"
          id="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>

      {/* Notes */}
      <div>
        <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-1">
          Notes (optional)
        </label>
        <textarea
          id="notes"
          name="notes"
          rows="3"
          value={formData.notes}
          onChange={handleChange}
          placeholder="How was your day? Any specific events or thoughts?"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none"
        />
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={!formData.mood || loading}
        className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
      >
        {loading ? 'Adding...' : 'Add Mood Entry'}
      </button>
    </form>
  );
}

export default MoodEntryForm;
