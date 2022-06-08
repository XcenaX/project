import numpy as np

# TODO: учесть расписание каждого из сотрудников до распределения (выходные)
# TODO: Сделать адекватное распределение задач между участниками
# 1) Нахождение первичного распределения с помощью венгерского алгоритма
# 2) Если задач больше, чем людей - найти доп. назначения в соответствии с графом задач
# 2.0) Проверяется каждая задача по порядку
# 2.1) Проводится поиск задач, параллельных заданной (отдельной функцией)
# 2.2) Если среди паралл. задач есть те, которые не может делать один человек, то...
# 2.2.1) Если на вторую паралл. задачу есть назначение, убираем из рассмотрения назначенного сотрудника
# 2.3) Назначаем на задачу сотрудника из доступных, способного выполнить ее за наименьшее количество времени
# 2.4) Переходим к 2.1 для следующей задачи
# TODO: Сделать вычисление количества дней на основе распределения и графа задач [FINISHED]
# 1) Проверяется последовательно каждая задача
# 2.1) Если у текущей задачи есть родитель, к количеству дней текущей
#    задачи прибавляется суммарное количество дней у родителя
# 2.2) Если родителя нет - счет идет с нуля (первая задача)
# TODO: Сделать вывод диаграммы Ганта (визуальная информация)
# TODO: Сделать вывод теоретических сроков выполнения проекта (с учетом распределения и выходных)

# matrix = np.array([
#     [3, 5, 1, 8, 12, 7, 3],
#     [6, 2, 2, 6, 14, 11, 4],
#     [4, 3, 1, 7, 10, 8, 3],
#     np.zeros(7),
#     np.zeros(7),
#     np.zeros(7),
#     np.zeros(7)
# ])

# zero task - begin of the project
# matrix = np.array([
#     [7, 6, 3],
#     [5, 4, 6],
#     [5, 7, 5]
# ])
# sequencing = np.array([
#     [0, 1, 1],
#     [0, 0, 0],
#     [0, 0, 0]
# ])
# parallel_by_one = [1, 2]
# path = [5, 4, 3]

# matrix = np.array([
#     [3, 5, 1, 8, 12, 7, 3],
#     [6, 2, 2, 6, 14, 11, 4],
#     [4, 3, 1, 7, 10, 8, 3]
# ])
# sequencing = np.array([
#     [0, 1, 0, 1, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0]
# ])
# parallel_by_one = [1, 3]

# matrix = np.array([
#     [8, 6, 10, 7],
#     [4, 5, 9, 8],
#     [7, 8, 12, 7]
# ])
# sequencing = np.array([
#     [0, 1, 0, 0],
#     [0, 0, 1, 1],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0]
# ])
# parallel_by_one = [2, 3]

# matrix = np.array([
#     [4, 5, 7, 6, 3],
#     [5, 7, 4, 7, 4],
#     [4, 8, 6, 6, 2],
#     [6, 7, 5, 5, 1]
# ])
# sequencing = np.array([
#       1  2  3  4  5
#     1[0, 0, 1, 0, 0],
#     2[0, 0, 1, 0, 0],
#     3[0, 0, 0, 1, 0],
#     4[0, 0, 0, 0, 1],
#     5[0, 0, 0, 0, 0]
# ])
# parallel_by_one = []

matrix = np.array([
    [7, 4, 8, 10, 19, 5, 11, 5],
    [5, 3, 11, 10, 13, 4, 7, 4],
    [8, 4, 12, 7, 18, 2, 9, 6],
    [10, 4, 7, 8, 21, 3, 12, 6]
])
sequencing = np.array([
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
parallel_by_one = [1, 2, 6, 7]


# def gantt(person_list, path_cells, path_costs, tasks_seq):  # не работает полностью
#     diagram = []
#     for i in range(len(path_cells)):
#         diagram.append([path_cells[i][0], [0, path_costs[i]]])
#     # diagram = [["C", [0, 5]], ["B", [0, 4]], ["A", [0, 3]]]
#     tasks_seq_t = np.transpose(tasks_seq)
#     for i in range(tasks_seq_t.shape[0]):
#         for j in range(tasks_seq_t.shape[1]):
#             if tasks_seq_t[i][j]:
#                 diagram[i][1][0] += diagram[j][1][1]
#     diagram = sorted(diagram, key=lambda lf: lf[0])
#     for i in diagram:
#         print(person_list[i[0]] + "] ", end='')
#         print(" " * i[1][0], end='')
#         print("#" * i[1][1])

class OptimalDistribution():
    def __init__(self, data_matrix, sequencing, parallel_by_one):
        self.data_matrix = data_matrix
        self.sequencing = sequencing
        self.parallel_by_one = parallel_by_one

    def solve(self):
        if self.data_matrix.shape[0] > self.data_matrix.shape[1]:
            raise AssertionError("Ошибка!!!!") from BaseException
        f = self.hungarian(self.data_matrix)
        assigned_tasks = [i[1] for i in f]
        if self.data_matrix.shape[0] != self.data_matrix.shape[1]:
            data_matrix_t = np.transpose(self.data_matrix)
            for i in range(data_matrix_t.shape[0]):
                if i not in assigned_tasks:
                    for j in range(data_matrix_t.shape[1]):
                        if i != j:
                            if not self.is_sequential(i, j):
                                if i in self.parallel_by_one and j in self.parallel_by_one:
                                    if j in assigned_tasks:
                                        for k in f:
                                            if k[1] == j:
                                                data_matrix_t[i][k[0]] = np.max(data_matrix_t[i] + 1)
                    f.append((np.argmin(data_matrix_t[i]), i))
                    assigned_tasks.append(i)
        f = sorted(f, key=lambda lf: lf[1])
        path_r = []
        for i in f:
            path_r.append(self.data_matrix[i])
        days = self.calculating_days(path_r)
        return [f, path_r, days]

    def reduce(self, source_matrix):
        # редукция по строкам
        w_matrix = np.copy(source_matrix)
        for i in range(w_matrix.shape[0]):
            w_matrix[i] -= np.min(w_matrix[i])
        
        # редукция по столбцам
        w_matrix = np.transpose(w_matrix)
        for i in range(w_matrix.shape[0]):
            w_matrix[i] -= np.min(w_matrix[i])
        w_matrix = np.transpose(w_matrix)
        return w_matrix

    def hungarian(self, source_matrix):
        modded_matrix = np.copy(source_matrix)
        if modded_matrix.shape[0] < modded_matrix.shape[1]:
            for i in range(modded_matrix.shape[1] - modded_matrix.shape[0]):
                modded_matrix = np.append(modded_matrix, np.zeros((1, modded_matrix.shape[1]), dtype=int), axis=0)
        modded_matrix = self.reduce(modded_matrix)
        mark_zero = []
        mark_zero_modified = []
        zeros = 0
        while zeros < modded_matrix.shape[0]:
            zero_matrix, mark_zero = self.find_path(modded_matrix)
            zeros = len(mark_zero)
            marked_rows, marked_cols = self.mark_matrix(zero_matrix, mark_zero)
            modded_matrix = self.adjust_matrix(modded_matrix, marked_rows, marked_cols)
        for i in range(len(mark_zero)):
            if mark_zero[i][0] < source_matrix.shape[0]:
                mark_zero_modified.append(mark_zero[i])
        return mark_zero_modified

    def calculate(self, source_matrix, path):  # только для квадратных матриц
        result = 0
        print(path)
        for it in range(len(path)):
            result += source_matrix[path[it][0], path[it][1]]
        return result

    def find_path(self, current_matrix):
        # нахождение максимального паросочетания (максимальное количество работников на максимальное количество работ)
        mark_zero = []
        zero_matrix = (current_matrix == 0)
        zero_matrix_marked = np.copy(zero_matrix)
        while np.sum(zero_matrix_marked) > 0:
            min_nonzero = zero_matrix_marked.shape[0]
            min_zeros_row = 0
            for i in range(zero_matrix_marked.shape[0]):
                if np.count_nonzero(zero_matrix_marked[i]) != 0 and np.count_nonzero(zero_matrix_marked[i]) < min_nonzero:
                    min_nonzero = np.count_nonzero(zero_matrix_marked[i])
                    min_zeros_row = i
            zero_index_col = np.where(zero_matrix_marked[min_zeros_row])[0][0]
            mark_zero.append((min_zeros_row, zero_index_col))
            zero_matrix_marked[min_zeros_row, :] = False
            zero_matrix_marked[:, zero_index_col] = False
        return zero_matrix, mark_zero

    def mark_matrix(self, zero_matrix, mark_zero):
        # разметка матрицы
        mark_zero_row_indices = [i[0] for i in mark_zero]
        non_marked_zero_rows = list(set(range(zero_matrix.shape[0])) - set(mark_zero_row_indices))
        marked_cols = []
        check_switch = True
        while check_switch:
            check_switch = False
            for i in non_marked_zero_rows:
                row_array = zero_matrix[i]
                for j in range(len(row_array)):
                    if row_array[j] and j not in marked_cols:
                        marked_cols.append(j)
                        check_switch = True
                for row_num, col_num in mark_zero:
                    if row_num not in non_marked_zero_rows and col_num in marked_cols:
                        non_marked_zero_rows.append(row_num)
                        check_switch = True
        marked_rows = list(set(range(zero_matrix.shape[0])) - set(non_marked_zero_rows))
        return marked_rows, marked_cols

    def adjust_matrix(self, current_matrix, marked_rows, marked_cols):
        # подстройка матрицы (добавление нулей)
        min_non_marked = np.max(current_matrix)
        adjusted_matrix = np.copy(current_matrix)
        for i in range(len(adjusted_matrix)):
            if i not in marked_rows:
                for j in range(len(adjusted_matrix[i])):
                    if j not in marked_cols:
                        if adjusted_matrix[i][j] < min_non_marked:
                            min_non_marked = adjusted_matrix[i][j]
        for i in range(len(adjusted_matrix)):
            if i not in marked_rows:
                for j in range(len(adjusted_matrix[i])):
                    if j not in marked_cols:
                        adjusted_matrix[i][j] -= min_non_marked
            else:
                for j in range(len(adjusted_matrix[i])):
                    if j in marked_cols:
                        adjusted_matrix[i][j] += min_non_marked
        return adjusted_matrix

    def calculating_days(self, path_r):
        sums = np.zeros(self.sequencing.shape[0], dtype=int)
        self.sequencing = np.transpose(self.sequencing)
        for i in range(self.sequencing.shape[0]):
            if 1 not in self.sequencing[i]:
                sums = np.insert(np.delete(sums, i), i, path_r[i])
            for j in range(self.sequencing.shape[1]):
                if self.sequencing[i][j] and sums[i] <= sums[j] + path_r[i]:
                    sums = np.insert(np.delete(sums, i), i, sums[j] + path_r[i])
        return np.max(sums)        

    def is_sequential(self, u1, u2):
        if u1 > u2:
            u1, u2 = u2, u1
        seq = (self.sequencing == 1)
        self.sequencing = np.transpose(seq)
        for k in range(self.sequencing.shape[0]):
            parents = []
            for j in range(self.sequencing.shape[1]):
                if self.sequencing[k][j]:
                    parents.append(j)
            for j in parents:
                self.sequencing[k] += self.sequencing[j]
        if self.sequencing[u2][u1]:  # direct connections
            return True
        else:
            for k in range(seq.shape[0]):
                if self.sequencing[u1][k] and self.sequencing[u2][k]:
                    return False

# print(self.hungarian(matrix))
# distr = OptimalDistribution(matrix, sequencing, parallel_by_one)
# try:
#     result = distr.solve()
#     print(result)
# except AssertionError:
#     print("Error!")

# for i in range(len(sequencing)):
#     print(i + 1, 'and 6 are', 'sequential' if is_sequential(sequencing, i, 5) else 'parallel')