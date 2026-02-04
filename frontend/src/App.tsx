import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import CourseCard from './components/CourseCard';
import { fetchCourses, Course, Filters } from './api';

function App() {
    const [courses, setCourses] = useState<Course[]>([]);
    const [filters, setFilters] = useState<Filters>({});
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        const loadCourses = async () => {
            setLoading(true);
            try {
                const data = await fetchCourses(filters);
                setCourses(data);
            } catch (error) {
                console.error("Failed to fetch courses:", error);
            } finally {
                setLoading(false);
            }
        };
        loadCourses();
    }, [filters]);

    return (
        <div className="flex bg-gray-100 min-h-screen">
            <Sidebar onFilterChange={setFilters} />
            
            <div className="ml-64 flex-1 p-8">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">KC Overseas Operations Portal</h1>
                    <p className="text-gray-600 mt-2">Find the perfect course and university for your students.</p>
                </header>

                {loading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {courses.length > 0 ? (
                            courses.map(course => (
                                <CourseCard key={course.course_id} course={course} />
                            ))
                        ) : (
                            <div className="col-span-full text-center py-10 text-gray-500">
                                No courses found matching your criteria.
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
