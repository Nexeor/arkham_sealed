import Header from "./components/Header";
import MainPanel from "./components/MainPanel";
import SetList from "./components/SetList";

function App() {
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
          <MainPanel></MainPanel>
        </div>
      </div>
      <div className="row bg-dark">Footer</div>
    </div>
  );
}

export default App;
