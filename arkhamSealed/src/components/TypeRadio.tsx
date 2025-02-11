interface Props {
  setSelected: (selectedType: string) => void;
  selected: string;
}

const TypeRadio = ({ setSelected, selected }: Props) => {
  const labels = ["All", "Investigator", "Player Cards", "Mythos"];

  return (
    <div className="btn-group">
      {labels.map((label) => {
        const id = label;
        return (
          <div key={id}>
            <input
              type="radio"
              className="btn-check"
              name="btnradio"
              id={id}
              autoComplete="off"
              checked={selected === id}
              onChange={() => setSelected(id)}
            />
            <label className="btn btn-outline-primary" htmlFor={id}>
              {label}
            </label>
          </div>
        );
      })}
    </div>
  );
};

export default TypeRadio;
