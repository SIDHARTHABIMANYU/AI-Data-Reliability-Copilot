import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastProvider } from './hooks/useToast';
import { AppLayout } from './components/layout/AppLayout';
import { OverviewPage } from './pages/OverviewPage';
import { PipelineMonitoringPage } from './pages/PipelineMonitoringPage';
import { DataQualityPage } from './pages/DataQualityPage';
import { AnomalyDetectionPage } from './pages/AnomalyDetectionPage';
import { IncidentsPage } from './pages/IncidentsPage';
import { InvestigationPage } from './pages/InvestigationPage';
import { RemediationPage } from './pages/RemediationPage';

export function App() {
  return (
    <ToastProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<OverviewPage />} />
            <Route path="/pipelines" element={<PipelineMonitoringPage />} />
            <Route path="/quality" element={<DataQualityPage />} />
            <Route path="/anomalies" element={<AnomalyDetectionPage />} />
            <Route path="/incidents" element={<IncidentsPage />} />
            <Route path="/investigation" element={<InvestigationPage />} />
            <Route path="/remediation" element={<RemediationPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  );
}

export default App;
