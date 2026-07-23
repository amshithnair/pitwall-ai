import { create } from 'zustand'

interface AuthState {
  token: str | null;
  role: str | null;
  login: (token: str, role: str) => void;
  logout: () => void;
}

interface TelemetryState {
  latestTelemetry: any | null;
  predictions: any[];
  addPrediction: (pred: any) => void;
  updateTelemetry: (data: any) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  role: null,
  login: (token, role) => set({ token, role }),
  logout: () => set({ token: null, role: null }),
}))

export const useTelemetryStore = create<TelemetryState>((set) => ({
  latestTelemetry: null,
  predictions: [],
  updateTelemetry: (data) => set({ latestTelemetry: data }),
  addPrediction: (pred) => set((state) => ({ predictions: [...state.predictions, pred] })),
}))
