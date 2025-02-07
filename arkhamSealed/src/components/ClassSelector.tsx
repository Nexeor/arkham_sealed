const classes = [
  "guardian",
  "seeker",
  "rogue",
  "mystic",
  "survivor",
  "neutral",
];

interface Props {
  onSelect: (selectedClass: string) => void;
}

const ClassSelector = ({ onSelect }: Props) => {
  return (
    <>
      <select
        className="form-select form-select-lg mb-3"
        onChange={(e) => onSelect((e.target as HTMLSelectElement).value)}
      >
        <option selected value="">
          Select Class
        </option>
        {classes.map((cls) => (
          <option key={cls} value={cls}>
            {cls.charAt(0).toUpperCase() + cls.slice(1)}
          </option>
        ))}
      </select>
    </>
  );
};

export default ClassSelector;
