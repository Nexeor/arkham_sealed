import { useState } from "react";
import Header from "./components/Header";
import MainPanel from "./components/MainPanel";
import SetList from "./components/SetList";

export interface CardQuery {
  id: number;
  name: string;
  cycle: string;
  type: string;
  faction: string;
}

function App() {
  const [cardQuery, setCardQuery] = useState<CardQuery>({} as CardQuery);
  const [selectedType, setSelectedType] = useState("All");

  return (
    <div className="container-fluid">
      <div className="row bg-info">
        <div className="col">
          <Header setSelected={setSelectedType} selected={selectedType} />
        </div>
      </div>
      <div className="row flex-grow-1">
        <div className="col-2 bg-primary p-0 m-0 ">
          <SetList />
        </div>
        <div className="col col-10 bg-secondary">
          <MainPanel cardQuery={cardQuery}></MainPanel>
        </div>
      </div>
      <div className="row bg-dark">Footer</div>
    </div>
  );
}

export default App;
