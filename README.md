# Formfolk — prompt to SVG

Generate a simple SVG illustration from a text prompt. The backend uses LangChain's tool calling with LangGraph to draw and review the SVG, and the Next.js page previews and downloads the result.

## Run the app

1. Set `OPENAI_API_KEY` in your environment.
2. Start the FastAPI backend from the repository root:

   ```bash
   poetry run uvicorn app.main:app --app-dir src --reload
   ```

3. Start the frontend:

   ```bash
   cd src/frontend
   npm run dev
   ```

Open [http://localhost:3000](http://localhost:3000). The page sends prompts to `http://localhost:8000/svgdrawer`. Set `NEXT_PUBLIC_API_URL` if the API runs at a different origin.

## API

`POST /svgdrawer` accepts `{ "prompt": "A blue whale beneath the stars" }` and returns an `image/svg+xml` file. Prompts must contain 1–500 characters.

## SVG art direction

Generated illustrations use a 300 × 200 canvas with an 18-unit safe margin and a centered subject that fills about 55–70% of the canvas height. The default style is a flat, soft-edged vector illustration with a clear silhouette and 8–18 purposeful shapes. Paired features should have consistent proportions, and small identifying details should remain readable.

The default palette is limited to five colors: cream `#F7F3E8`, dark brown outline `#3D342F`, leaf green `#78966B`, warm yellow `#E8B95B`, and coral `#D97862`. Main outlines use the dark brown at 2.5–3 units with rounded joins/caps where applicable. User-requested styles can override the default style while keeping the layout legible.

The drawer supports SVG `path` shapes with `M`, `L`, `H`, `V`, `C`, `S`, `Q`, `T`, `A`, and `Z` commands. Use cubic/quadratic curves for organic silhouettes and details. Path data is length-limited and restricted to SVG path command characters before it is added to the document.
