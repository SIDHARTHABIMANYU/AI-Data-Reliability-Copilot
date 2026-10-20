import { useState, useEffect, useCallback, createContext, useContext } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { TopNav } from './TopNav';
import { checkSystemHealth } from '../../services/dashboardService';
import { SystemHealth } from '../../types/api';

interface RefreshContextType {
  lastRefreshed: Date | null;
  triggerRefresh: () => void;
  refreshCount: number;
}

export const RefreshContext = createContext<RefreshContextType>({
  lastRefreshed: null,
  triggerRefresh: () => {},
  refreshCount: 0,
});

export function useGlobalRefresh() {
  return useContext(RefreshContext);
}

export function AppLayout() {
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [lastRefreshed, setLastRefreshed] = useState<Date | null>(new Date());
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [refreshCount, setRefreshCount] = useState(0);

  const fetchHealth = useCallback(async () => {
    const res = await checkSystemHealth();
    setHealth(res);
  }, []);

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, [fetchHealth]);

  const handleManualRefresh = useCallback(async () => {
    setIsRefreshing(true);
    await fetchHealth();
    setLastRefreshed(new Date());
    setRefreshCount((prev) => prev + 1);
    setTimeout(() => {
      setIsRefreshing(false);
    }, 400);
  }, [fetchHealth]);

  return (
    <RefreshContext.Provider
      value={{
        lastRefreshed,
        triggerRefresh: handleManualRefresh,
        refreshCount,
      }}
    >
      <div className="min-h-screen bg-[#06090e] text-slate-100 flex flex-col">
        <Sidebar
          health={health}
          isOpen={mobileSidebarOpen}
          onCloseMobile={() => setMobileSidebarOpen(false)}
        />

        <div className="flex-1 flex flex-col lg:pl-64">
          <TopNav
            health={health}
            lastRefreshed={lastRefreshed}
            isRefreshing={isRefreshing}
            onRefresh={handleManualRefresh}
            onOpenMobileMenu={() => setMobileSidebarOpen(true)}
            error={!health?.isOnline ? 'Backend offline (FastAPI port 8000)' : null}
          />

          <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
            <Outlet />
          </main>

          <footer className="py-4 px-6 border-t border-slate-800/60 text-xs font-mono text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-2">
            <div>AI Data Reliability Copilot — Observability & Incident Response</div>
            <div className="flex items-center gap-4">
              <span>FastAPI + PostgreSQL</span>
              <span>•</span>
              <span>LangGraph + AWS Bedrock</span>
              <span>•</span>
              <span>Pinecone RAG</span>
            </div>
          </footer>
        </div>
      </div>
    </RefreshContext.Provider>
  );
}
