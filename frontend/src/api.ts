import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Course {
    course_id: number;
    uni_id: number;
    course_name: string;
    level_code: string;
    intake_months: string;
    tuition_fee: number;
    is_stem: boolean;
    has_internship: boolean;
    min_ielts_overall: number;
    min_gpa_ug: number;
    backlog_limit: number;
    is_moi_accepted: boolean;
    university?: {
        name: string;
        country: string;
        logo_url?: string;
    };
}

export interface Filters {
    min_gpa?: number;
    max_tuition?: number;
    ielts_score?: number;
    backlogs?: number;
    is_stem?: boolean;
}

export const fetchCourses = async (filters: Filters) => {
    const params = new URLSearchParams();
    if (filters.min_gpa) params.append('min_gpa', filters.min_gpa.toString());
    if (filters.max_tuition) params.append('max_tuition', filters.max_tuition.toString());
    if (filters.ielts_score) params.append('ielts_score', filters.ielts_score.toString());
    if (filters.backlogs) params.append('backlogs', filters.backlogs.toString());
    if (filters.is_stem !== undefined) params.append('is_stem', filters.is_stem.toString());

    const response = await axios.get<Course[]>(`${API_URL}/search`, { params });
    return response.data;
};
