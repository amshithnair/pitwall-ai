"use client";

import { useEffect, useRef, useState } from 'react';
import { useAuthStore, useTelemetryStore } from '@/store/useStore';

export function WebSocketProvider({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((state) => state.token);
  const updateTelemetry = useTelemetryStore((state) => state.updateTelemetry);
  const addPrediction = useTelemetryStore((state) => state.addPrediction);
  const ws = useRef<WebSocket | null>(null);
  
  useEffect(() => {
    if (!token) return;
    
    const connect = () => {
      ws.current = new WebSocket(`ws://localhost:8008/ws?token=${token}`);
      
      ws.current.onmessage = (event) => {
        if (event.data === "pong") return;
        try {
          const data = JSON.parse(event.data);
          if (data.event_type.startsWith('prediction.')) {
            addPrediction(data);
          } else {
            updateTelemetry(data);
          }
        } catch (e) {
          console.error("Error parsing WS message", e);
        }
      };
      
      ws.current.onclose = () => {
        setTimeout(connect, 2000); // Auto reconnect
      };
    };
    
    connect();
    
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [token, updateTelemetry, addPrediction]);
  
  return <>{children}</>;
}
