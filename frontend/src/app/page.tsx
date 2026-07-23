"use client";

import { useEffect, useState } from 'react';
import { useTelemetryStore, useAuthStore } from '@/store/useStore';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Dashboard() {
  const token = useAuthStore(state => state.token);
  const router = useRouter();
  const latestTelemetry = useTelemetryStore(state => state.latestTelemetry);
  const predictions = useTelemetryStore(state => state.predictions);
  
  // Keep history of speed for chart
  const [speedHistory, setSpeedHistory] = useState<{time: string, speed: number}[]>([]);

  useEffect(() => {
    if (!token) {
      router.push('/login');
    }
  }, [token, router]);

  useEffect(() => {
    if (latestTelemetry?.payload) {
      try {
        // Very basic parsing for milestone demo
        const payloadStr = latestTelemetry.payload;
        // In real app, we parse the JSON payload from the WS
        // Just mock updating speed if available or random for visual
        const newSpeed = Math.floor(Math.random() * 50) + 250; 
        setSpeedHistory(prev => {
          const next = [...prev, { time: new Date().toLocaleTimeString(), speed: newSpeed }];
          return next.slice(-20); // Keep last 20 points
        });
      } catch(e) {}
    }
  }, [latestTelemetry]);

  if (!token) return null;

  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-300">
      <header className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-bold text-white tracking-wide">PITWALL AI</h1>
          <span className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded font-mono border border-green-500/30">LIVE</span>
        </div>
        <nav className="flex gap-4">
          <Link href="/chat" className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded text-sm transition-colors border border-slate-700">AI Race Engineer</Link>
        </nav>
      </header>

      <main className="flex-1 p-6 grid grid-cols-1 lg:grid-cols-3 gap-6 overflow-y-auto">
        
        {/* Live Timing / Telemetry */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-lg">
            <h2 className="text-lg font-semibold text-white mb-4 flex items-center justify-between">
              Live Telemetry 
              <span className="text-xs text-slate-500 font-mono">{latestTelemetry?.driver_id || 'Waiting...'}</span>
            </h2>
            <div className="h-64 flex items-end justify-between gap-1">
              {/* Very primitive bar chart for visual before Recharts handles it in full prod */}
              {speedHistory.map((pt, i) => (
                <div key={i} className="w-full bg-blue-500/20 hover:bg-blue-500/40 rounded-t transition-all relative group" style={{ height: `${(pt.speed / 350) * 100}%` }}>
                  <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-xs py-1 px-2 rounded opacity-0 group-hover:opacity-100">{pt.speed}</div>
                </div>
              ))}
              {speedHistory.length === 0 && <div className="w-full text-center text-slate-600 my-auto">No telemetry data yet...</div>}
            </div>
            <div className="mt-4 flex justify-between text-xs text-slate-500 border-t border-slate-800 pt-4">
              <span>0s</span>
              <span>Speed (km/h) Trace</span>
              <span>Now</span>
            </div>
          </div>
        </div>

        {/* Strategy & Predictions Sidebar */}
        <div className="space-y-6">
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-lg">
            <h2 className="text-lg font-semibold text-white mb-4">ML Predictions</h2>
            <div className="space-y-4">
              {predictions.length > 0 ? predictions.slice(-3).map((p, i) => (
                <div key={i} className="p-3 bg-slate-800 rounded border border-slate-700">
                  <div className="text-xs text-slate-400 font-mono mb-1">{p.event_type}</div>
                  <div className="text-sm text-slate-200">{p.payload}</div>
                </div>
              )) : (
                <div className="text-sm text-slate-500 italic">No predictions generated yet. Waiting for Lap complete event.</div>
              )}
            </div>
          </div>

          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-lg">
            <h2 className="text-lg font-semibold text-white mb-4">Active Strategy</h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-slate-800 rounded border border-slate-700">
                <span className="text-sm text-slate-400">Current Compound</span>
                <span className="text-sm font-semibold text-yellow-400">MEDIUM (M)</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-800 rounded border border-slate-700">
                <span className="text-sm text-slate-400">Tyre Age</span>
                <span className="text-sm font-mono text-white">12 Laps</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-800 rounded border border-slate-700">
                <span className="text-sm text-slate-400">Pit Window</span>
                <span className="text-sm font-mono text-green-400">Lap 15 - 18</span>
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}
