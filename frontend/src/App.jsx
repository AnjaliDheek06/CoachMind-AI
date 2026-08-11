import { Routes, Route } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import GenerateLessonPage from "./pages/GenerateLessonPage";
import LessonPage from "./pages/LessonPage";
import ScenarioPage from "./pages/ScenarioPage";
import PracticeFeedbackPage from "./pages/PracticeFeedbackPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<UploadPage />} />
      <Route path="/generate-lesson" element={<GenerateLessonPage />} />
      <Route path="/lesson/:lessonId" element={<LessonPage />} />
      <Route path="/scenario" element={<ScenarioPage />} />
      <Route path="/practice-feedback" element={<PracticeFeedbackPage />} />
    </Routes>
  );
}

export default App;