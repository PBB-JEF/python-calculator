import React from 'react';

function MoodEntryList({ entries, onDeleteEntry }) {
  const getMoodEmoji = (mood) => {
    const moodEmojis = {
      'happy': '😊',
      'excited': '🤩',
      'calm': '😌',
      'sad': '😢',
      'anxious': '😰',
      'angry': '😠',
      'tired': '😴',
      'confused': '😕'
    };
    return moodEmojis[mood] || '😐';
  };

  const getMoodColor = (mood) => {
    const moodColors = {
      'happy': 'bg-green-100 text-green-800',
      'excited': 'bg-yellow-100 text-yellow-800',
      'calm': 'bg-blue-100 text-blue-800',
      'sad': 'bg-gray-100 text-gray-800',
      'anxious': 'bg-orange-100 text-orange-800',
      'angry': 'bg-red-100 text-red-800',
      'tired': 'bg-purple-100 text-purple-800',
      'confused': 'bg-indigo-100 text-indigo-800'
    };
    return moodColors[mood] || 'bg-gray-100 text-gray-800';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString('en-US', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
      });
    }
  };

  if (entries.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mx-auto h-12 w-12 text-gray-400 mb-4">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No mood entries yet</h3>
        <p className="text-gray-500">Start tracking your moods by adding your first entry!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {entries.map((entry) => (
        <div
          key={entry.id}
          className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-gray-300 transition-colors duration-200"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <span className="text-2xl">{getMoodEmoji(entry.mood)}</span>
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${getMoodColor(entry.mood)}`}>
                  {entry.mood}
                </span>
                <span className="text-sm text-gray-500">
                  {formatDate(entry.date)}
                </span>
              </div>
              
              {entry.notes && (
                <p className="text-gray-700 text-sm leading-relaxed">
                  {entry.notes}
                </p>
              )}
            </div>
            
            <button
              onClick={() => onDeleteEntry(entry.id)}
              className="ml-4 p-1 text-gray-400 hover:text-red-500 transition-colors duration-200"
              title="Delete entry"
            >
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default MoodEntryList;
