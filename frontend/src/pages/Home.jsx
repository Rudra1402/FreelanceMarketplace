import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen min-w-screen text-white flex flex-col justify-center items-center">
      <div className="px-6 py-16 text-center flex flex-col justify-center items-center">
        {/* Header Section */}
        <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600 mb-6">
          Welcome to the Marketplace
        </h1>
        <p className="text-lg text-gray-300 mb-12">
          Discover unique items, propose collaborations, and leave meaningful reviews in a thriving community.
        </p>

        {/* Features Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-[90%]">
          {/* Marketplace */}
          <Link
            to="/marketplace"
            className="rounded-lg shadow-lg bg-gray-800 hover:bg-blue-500 transition transform hover:-translate-y-2 duration-300 p-8 text-left"
          >
            <h2 className="text-3xl font-semibold text-blue-300">Marketplace</h2>
            <p className="text-gray-300 mt-4">
              Browse items and explore opportunities for buying and selling.
            </p>
          </Link>

          {/* Proposals */}
          <Link
            to="/proposals"
            className="rounded-lg shadow-lg bg-gray-800 hover:bg-blue-500 transition transform hover:-translate-y-2 duration-300 p-8 text-left"
          >
            <h2 className="text-3xl font-semibold text-blue-300">Proposals</h2>
            <p className="text-gray-300 mt-4">
              Propose collaborations or respond to offers from others.
            </p>
          </Link>

          {/* Ratings */}
          <Link
            to="/ratings"
            className="rounded-lg shadow-lg bg-gray-800 hover:bg-blue-500 transition transform hover:-translate-y-2 duration-300 p-8 text-left"
          >
            <h2 className="text-3xl font-semibold text-blue-300">Ratings</h2>
            <p className="text-gray-300 mt-4">
              Rate and review users to build trust in the community.
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;
