import React from 'react';

const AddRatingForm = () => {
  return (
    <form>
      <h2>Add Rating</h2>
      <select>
        <option>1</option>
        <option>2</option>
        <option>3</option>
        <option>4</option>
        <option>5</option>
      </select>
      <textarea placeholder="Write a comment..."></textarea>
      <button type="submit">Submit</button>
    </form>
  );
};

export default AddRatingForm;
