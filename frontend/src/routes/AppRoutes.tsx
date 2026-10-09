import { Navigate, Route, Routes } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import DocumentsPage from "../pages/DocumentsPage";
import ExplorePage from "../pages/ExplorePage";
import InsightsPage from "../pages/InsightsPage";
import ComparePage from "../pages/ComparePage";
import ReviewPage from "../pages/ReviewPage";

export default function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Navigate to="/documents" replace />} />
        <Route path="/documents" element={<DocumentsPage />} />
        <Route path="/explore" element={<ExplorePage />} />
        <Route path="/insights" element={<InsightsPage />} />
        <Route path="/compare" element={<ComparePage />} />
        <Route path="/review" element={<ReviewPage />} />
        <Route path="*" element={<Navigate to="/documents" replace />} />
      </Route>
    </Routes>
  );
}
