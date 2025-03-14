import { createBrowserRouter } from "react-router-dom";
import App from "../App";
import HomePage from "../pages/Home";
import ResultPage from "../pages/Result";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <HomePage />
      },
      {
        path: "result/:taskId",
        element: <ResultPage />,
        loader: async ({ params }) => {
          const response = await fetch(`/api/tasks/${params.taskId}`);
          return response.json();
        }
      }
    ]
  }
]);

export default router;
