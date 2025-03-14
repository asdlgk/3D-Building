import React from 'react';
import './style.css';

export default function ProgressBar({ progress }) {
  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="progress-ring">
      <svg width="120" height="120">
        <circle
          className="progress-ring__background"
          strokeWidth="8"
          fill="transparent"
          r={radius}
          cx="60"
          cy="60"
        />
        <circle
          className="progress-ring__foreground"
          strokeWidth="8"
          fill="transparent"
          strokeDasharray={`${circumference} ${circumference}`}
          strokeDashoffset={offset}
          r={radius}
          cx="60"
          cy="60"
        />
      </svg>
      <div className="progress-text">{Math.round(progress)}%</div>
    </div>
  );
}
