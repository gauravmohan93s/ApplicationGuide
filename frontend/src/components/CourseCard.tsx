import React from 'react';
import { Course } from '../api';

interface CourseCardProps {
    course: Course;
}

const CourseCard: React.FC<CourseCardProps> = ({ course }) => {
    return (
        <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300 border border-gray-100">
            <div className="p-5">
                <div className="flex justify-between items-start">
                    <div>
                        <h3 className="text-lg font-bold text-gray-900 line-clamp-2">{course.course_name}</h3>
                        <p className="text-sm text-indigo-600 font-medium mt-1">{course.university?.name}</p>
                    </div>
                    {course.university?.logo_url && (
                        <img src={course.university.logo_url} alt="Logo" className="h-10 w-10 object-contain" />
                    )}
                </div>

                <div className="mt-4 grid grid-cols-2 gap-4 text-sm text-gray-600">
                    <div>
                        <span className="block text-xs text-gray-400 uppercase tracking-wide">Tuition</span>
                        <span className="font-semibold text-gray-800">£{course.tuition_fee.toLocaleString()}</span>
                    </div>
                    <div>
                        <span className="block text-xs text-gray-400 uppercase tracking-wide">Level</span>
                        <span className="font-semibold text-gray-800">{course.level_code || 'N/A'}</span>
                    </div>
                    <div>
                        <span className="block text-xs text-gray-400 uppercase tracking-wide">Min GPA</span>
                        <span className="font-semibold text-gray-800">{course.min_gpa_ug || '-'}</span>
                    </div>
                    <div>
                        <span className="block text-xs text-gray-400 uppercase tracking-wide">IELTS</span>
                        <span className="font-semibold text-gray-800">{course.min_ielts_overall || '-'}</span>
                    </div>
                </div>

                <div className="mt-4 flex flex-wrap gap-2">
                    {course.is_stem && (
                        <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">STEM</span>
                    )}
                    {course.has_internship && (
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">Internship</span>
                    )}
                    {course.is_moi_accepted && (
                        <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded-full">MOI Accepted</span>
                    )}
                </div>
            </div>
            <div className="bg-gray-50 px-5 py-3 border-t border-gray-100 flex justify-between items-center">
                 <span className="text-xs text-gray-500">Backlogs: {course.backlog_limit}</span>
                 <button className="text-sm text-indigo-600 font-medium hover:text-indigo-800">View Factsheet →</button>
            </div>
        </div>
    );
};

export default CourseCard;
