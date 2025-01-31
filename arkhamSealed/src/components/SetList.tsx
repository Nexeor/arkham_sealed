const SetList = () => {
  const setList = [
    "Core Set",
    "Dunwich Legacy",
    "Path to Carcosa",
    "Forgotten Age",
    "Circle Undone",
    "Dream-Eaters",
    "Innsmouth Conspiracy",
    "Edge of the Earth",
    "Scarlet Keys",
    "Feast of Hemlock Vale",
    "Drowned City",
  ];
  return (
    <div className="btn-group-vertical">
      {setList.map((set) => {
        return (
          <button className="btn btn-primary" key={set}>
            {set}
          </button>
        );
      })}
    </div>
  );
};

export default SetList;
