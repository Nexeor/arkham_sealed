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
    <div className="btn-group-vertical text-white bg-primary w-100">
      <h4 className="text-center m-2">Browse by Set:</h4>
      {setList.map((set) => {
        return (
          <button className="btn btn-primary w-100 text-start" key={set}>
            {set}
          </button>
        );
      })}
    </div>
  );
};

export default SetList;
