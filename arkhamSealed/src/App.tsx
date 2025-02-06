import { useState } from "react";
import Header from "./components/Header";
import MainPanel from "./components/MainPanel";
import SetList from "./components/SetList";

import { CardQuery } from "./hooks/useCards";

function App() {
  const [cardQuery, setCardQuery] = useState<CardQuery>({} as CardQuery);

  return (
    <div className="container-fluid">
      <div className="row bg-info">
        <div className="col">
          <Header />
        </div>
      </div>
      <div className="row">
        <div className="col-1 bg-primary">
          <SetList />
        </div>
        <div className="col bg-secondary">
          <MainPanel cardQuery={cardQuery}></MainPanel>
        </div>
      </div>
      <div className="row bg-dark">Footer</div>
    </div>
  );
}

export default App;
