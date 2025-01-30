import React from 'react';

const MarketplaceItemDetails = ({ title, description, minPrice, maxPrice }) => {
  return (
    <div className="bg-gray-900 text-white min-h-screen py-16 px-6">
      <div className="container mx-auto">
        <h2 className="text-4xl font-bold text-blue-400 mb-6">{title}</h2>
        <p className="text-gray-300 mb-4">{description}</p>
        <p className="text-lg text-gray-300">
          <span className="font-semibold text-blue-400">Price Range:</span> ${minPrice} - ${maxPrice}
        </p>
      </div>
    </div>
  );
};

export default MarketplaceItemDetails;
